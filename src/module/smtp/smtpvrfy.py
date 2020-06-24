import threading,socket
import netaddr,os,re

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

class Module_SMTP_VRFY(Module):

    opt_static = {"target":target,"userfile":userfile}#{"target":target,"output":flag}
    opt_dynamic = {}#{"target":target,"output":flag}

    def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
        threading.Thread.__init__(self)
        super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

    # Validating user module options
    def validate(opt_dict=None):
        valid = True
        opt = dict(Module_SMTP_VRFY.opt_static)
        if opt_dict != None and len(opt_dict.keys()) >= len(Module_SMTP_VRFY.opt_static.keys()):
            for k,v in opt_dict.items():
                if k in Module_SMTP_VRFY.opt_static:
                    valid = valid and Module_SMTP_VRFY.opt_static.get(k,None)(v)
                    try:
                        opt.pop(k, None)
                    except:
                        print("{}".format(e))
                        print("{}".format(traceback.print_exc()))
                        return False
                elif k in Module_SMTP_VRFY.opt_dynamic:
                    valid = valid and Module_SMTP_VRFY.opt_dynamic.get(k,None)(v)
        
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
        return "Module_SMTP_VRFY"
    
    def printData(data=None,conn=None):
        if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
            conn.sendall((bcolors.OKBLUE+bcolors.BOLD+"\n".join(data)+bcolors.ENDC+"\n").encode()) 
        if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
            print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,"\n".join(data),bcolors.ENDC))

    def run(self):
        lst = Module_SMTP_VRFY.targets(self.opt_dict["target"])
        data = {}
        try:
            users = open(self.opt_dict["userfile"],"r")
        except:
            print("{}{}Error Opening file! Module: Module_SMTP_VRFY{}".format(bcolors.WARNING,ENDC,bcolors.BOLD,bcolors.ENDC))
            return
                
        for ip in lst:
            if not self.flag.is_set():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(60)
                try:
                    s.connect((ip.rstrip(),25))
                    s.recv(1024)
                except:
                    print("{}{}Unable to connect to {}{}".format(bcolors.WARNING,bcolors.BOLD,ip,bcolors.ENDC))
                    s.close()
                    continue
                gem = []
                for user in users:
                    s.send(('VRFY ' + user.rstrip() + '\r\n').encode())
                    try:
                        response = s.recv(1024).decode()
                        vrfy = re.search(user.rstrip(),response.rstrip())
                        if vrfy:
                            vrfy = re.search("unknown",response.rstrip())
                            if not vrfy:
                                gem.append(user.rstrip())
                    except Exception as e:
                        print(e)
                        break
                s.close()
                if len(gem) == 0:
                    gem.append("No valid user!")
                data[ip] = gem

                if self.mode == "profile":
                    fd = open(Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID']+"/profile/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/smtpvrfy","w")
                    fd.write("\n".join(gem))
                    fd.close()

                for val in gem:
                    if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as slogger:
                            slogger.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
                            try:
                                slogger.sendall((bcolors.OKBLUE+"[*]"+bcolors.ENDC+" "+bcolors.BOLD+val+bcolors.ENDC).encode())  
                            finally:
                                slogger.close()
                    if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
                        print("{}[*]{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,val,bcolors.ENDC))
            else:
                break
        #Store Data for Global query
        self.storeDataRegular(data)
        return
