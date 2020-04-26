import threading,socket
import netaddr,os,re

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

class Module_SMTP_VRFY(Module):

    opt = {"target":target,"userfile":userfile}#{"target":target,"output":flag}

    def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
        threading.Thread.__init__(self)
        super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

    # Validating user module options
    def validate(opt_dict):
        valid = True
        if len(opt_dict.keys()) == len(Module_SMTP_VRFY.opt.keys()):
            for k,v in opt_dict.items():
                valid = valid and Module_SMTP_VRFY.opt.get(k,None)(v)
        else:
            valid = False
        return valid
    
    def getName():
        return "Module_SMTP_VRFY"
    
    def printData(data=None,conn=None):
        if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True" and conn != None:
            conn.sendall((bcolors.OKBLUE+bcolors.BOLD+"\n".join(data)+bcolors.ENDC+"\n").encode()) 
        if Config.CLIENTVERBOSE == "True":
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
                    fd = open(Config.PATH+"/db/sessions/"+Config.SESSID+"/profiles/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/smtpvrfy","w")
                    fd.write("\n".join(gem))
                    fd.close()

                for val in gem:
                    if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as slogger:
                            slogger.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
                            try:
                                slogger.sendall((bcolors.OKBLUE+"[*]"+bcolors.ENDC+" "+bcolors.BOLD+val+bcolors.ENDC).encode())  
                            finally:
                                slogger.close()
                    if Config.CLIENTVERBOSE == "True":
                        print("{}[*]{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,val,bcolors.ENDC))
            else:
                break
        #Store Data for Global query
        self.storeDataRegular(data)
        return
