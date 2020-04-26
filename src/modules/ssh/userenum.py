import threading,socket
import netaddr,os,subprocess,re

from src.miscellaneous.config import Config,bcolors
from src.modules.module import Module

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

    opt = {"target":target, "userfile":userfile}

    def __init__(self,opt_dict,mode,module_name,profile_tag=None,profile_port=None):
        threading.Thread.__init__(self)
        super().__init__(opt_dict,mode,module_name,profile_tag,profile_port)

    # Validating user module options
    def validate(opt_dict):
        valid = True
        if len(opt_dict.keys()) == len(Module_SSH_userenum.opt.keys()):
            for k,v in opt_dict.items():
                valid = valid and Module_SSH_userenum.opt.get(k,None)(v)
        else:
            valid = False
        return valid
    
    def getName():
        return "Module_SSH_userenum"
    
    def printData(data=None,conn=None):
        if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True" and conn != None:
            conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode()) 
        if Config.CLIENTVERBOSE == "True":
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
                    proc = os.popen("python2 {}/3rd/enumSSH.py {} {}".format(Config.PATH,ip,user))
                    out = proc.read()
                    if re.match("^\[\+\] [a-zA-Z0-9-_ ]+$", out):
                        gem.append(out)
                    proc.close()                
                
                if len(gem) == 0:
                    gem.append("No user discovered!")
                
                if self.mode == "profile":
                    fd = open(Config.PATH+"/db/sessions/"+Config.SESSID+"/profiles/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/userenum","w")
                    fd.write("\n".join(gem))
                    fd.close()
                data[ip] = "\n".join(gem)
                self.storeDataRegular(data)
                if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
                        try:
                            s.sendall((bcolors.BOLD+("\n".join(gem))+bcolors.ENDC).encode()) 
                        finally:
                            s.close()
                if Config.CLIENTVERBOSE == "True":
                    print("{}{}{}".format(bcolors.BOLD,("\n".join(gem)),bcolors.ENDC))
            else:
                break
        return
