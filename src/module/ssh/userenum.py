import threading,socket
import netaddr,os,subprocess,re

from src.miscellaneous.config import Config,bcolors
from src.module.module import Module

import time

def target(val=None):
    if val is None:
        return False
    else:
        return bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val))

def userfile(val=None):
    if val is None:
        return False
    else:
        return os.path.isfile(val)

#Need to see how to deal with multiple flags
def flag(val=None):
    return True

class Module_SSH_userenum(Module):

    opt_static = {"target":target, "userfile":userfile}
    opt_dynamic = {}

    def __init__(self,opt_dict,mode,module_name,profile_tag=None,profile_port=None):
        threading.Thread.__init__(self)
        super().__init__(opt_dict,mode,module_name,profile_tag,profile_port)

    # Validating user module options
    def validate(opt_dict=None):
        valid = True
        opt = dict(Module_SSH_userenum.opt_static)
        if opt_dict != None and len(opt_dict.keys()) >= len(Module_SSH_userenum.opt_static.keys()):
            for k,v in opt_dict.items():
                if k in Module_SSH_userenum.opt_static:
                    valid = valid and Module_SSH_userenum.opt_static.get(k,None)(v)
                    try:
                        opt.pop(k, None)
                    except:
                        print("{}".format(e))
                        print("{}".format(traceback.print_exc()))
                        return False
                elif k in Module_SSH_userenum.opt_dynamic:
                    valid = valid and Module_SSH_userenum.opt_dynamic.get(k,None)(v)
        
            if len(opt) != 0:
                valid = False
            else:
                for option in opt:
                    print("{}{}Missing: {}{}".format(bcolors.FAIL,bcolors.BOLD,bcolors.ENDC,option))
        else:
            for option in opt:
                    print("{}{}Missing: {}{}".format(bcolors.FAIL,bcolors.BOLD,bcolors.ENDC,option))
            valid = False
            
        return valid
    
    def getName():
        return "Module_SSH_userenum"
    
    def printData(data=None,conn=None):
        if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
            conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode()) 
        if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
            print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,data,bcolors.ENDC))

    def run(self):
        lst = Module_SSH_userenum.targets(self.opt_dict["target"])
        data = {}
        try:
            users = open(self.opt_dict["userfile"],"r")
        except:
            print("{}{}Error Opening file! Module: Module_SSH_userenum{}".format(bcolors.WARNING,bcolors.BOLD,bcolors.ENDC))
            return

        for ip in lst:
            if not self.flag.is_set():
                gem = []
                for user in users:
                    proc = os.popen("python2 {}/3rd/enumSSH.py {} {}".format(Config.CONFIG['GENERAL']['PATH'],ip,user))
                    out = proc.read()
                    if re.match("^\[\+\] [a-zA-Z0-9-_ ]+$", out):
                        gem.append(out)
                    proc.close()                
                
                if len(gem) == 0:
                    gem.append("No user discovered!")
                
                if self.mode == "profile":
                    fd = open(Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID']+"/profile/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/userenum","w")
                    fd.write("\n".join(gem))
                    fd.close()
                data[ip] = "\n".join(gem)
                self.storeDataRegular(data)
                if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
                        try:
                            s.sendall((bcolors.BOLD+("\n".join(gem))+bcolors.ENDC).encode()) 
                        finally:
                            s.close()
                if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
                    print("{}{}{}".format(bcolors.BOLD,("\n".join(gem)),bcolors.ENDC))
            else:
                break
        return
