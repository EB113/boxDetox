import threading
import re

from src.menus.commons import State
from src.miscellaneous.config import Config,bcolors

class Module(threading.Thread):

    def __init__(self,opt_dict=None,mode=None,module_name=None,profile_tag=None,profile_port=None):
        self.flag = threading.Event()
        if opt_dict == None:
            raise ValueError("Module argument opt_dict is None!")
        self.opt_dict = opt_dict
        if mode == None:
            raise ValueError("Module argument mode is None!")
        self.mode = mode
        if module_name == None:
            raise ValueError("Module argument module_name is None!")
        self.module_name = module_name      
        #if profile_tag != None and profile_port == None:
            #raise ValueError("Profile argument profile_port is None!")
        self.profile_tag = profile_tag
        self.profile_port = profile_port
    
    @property
    def opt_static(self):
        raise NotImplementedError

    @property
    def opt_dynamic(self):
        raise NotImplementedError
    
    @classmethod
    def getName(cls):
        return cls.__name__
    
    @classmethod
    # Validating user module options
    def validate(cls,opt_dict=None):
        valid = True
        opt = dict(cls.opt_static)
        if opt_dict != None and len(opt_dict.keys()) >= len(cls.opt_static.keys()):
            for k,v in opt_dict.items():
                if k in cls.opt_static:
                    valid = valid and cls.opt_static.get(k,None)(v)
                    try:
                        opt.pop(k, None)
                    except:
                        print("{}".format(e))
                        print("{}".format(traceback.print_exc()))
                        return False
                elif k in cls.opt_dynamic:
                    valid = valid and cls.opt_dynamic.get(k,None)(v)

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

    @classmethod
    def printData(cls,data=None,conn=None,enclose=False):
        if data != None and len(data)>0:
            if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
                if enclose:
                    # Header
                    conn.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
                    conn.sendall((bcolors.BOLD+bcolors.OKGREEN+"Name:"+bcolors.ENDC+bcolors.BOLD+" "+cls.__name__+bcolors.ENDC+"\n").encode())
                # Body
                conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode())
                # Footer
                if enclose:
                    conn.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())

            if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
                if enclose:
                    # Header
                    print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,bcolors.ENDC))
                    print("{}{}Name:{} {}{}{}".format(bcolors.BOLD,bcolors.OKGREEN,bcolors.ENDC,bcolors.BOLD,cls.__name__,bcolors.ENDC))
                # Body
                print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,data,bcolors.ENDC))
                if enclose:
                    # Footer
                    print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,bcolors.ENDC))

    def storeDataPortscan(self,data):
        if self.mode == "module":
            if "portscan" not in State.moduleData:
                State.moduleData["portscan"] = {}
            if self.module_name not in State.moduleData["portscan"]:
                State.moduleData["portscan"][self.module_name] = {}
            for ip in data:
                State.moduleData["portscan"][self.module_name][ip] = data[ip]
        elif self.mode == "profile":
            if self.profile_tag != None:
                if self.profile_tag not in State.profileData:
                    State.profileData[self.profile_tag] = {}
                if "portscan" not in State.profileData[self.profile_tag]:
                    State.profileData[self.profile_tag]["portscan"] = {}
                if self.module_name != None:
                    if self.module_name not in State.profileData[self.profile_tag]["portscan"]:
                        State.profileData[self.profile_tag]["portscan"][self.module_name] = {}
                    for ip in data:
                        State.profileData[self.profile_tag]["portscan"][self.module_name][ip] = data[ip]
    
    def storeDataRegular(self,data):
        if self.mode == "module":
            if "regular" not in State.moduleData:
                State.moduleData["regular"] = {}
            if self.module_name not in State.moduleData["regular"]:
                State.moduleData["regular"][self.module_name] = {}
            for ip in data:
                State.moduleData["regular"][self.module_name][ip] = data[ip]
        elif self.mode == "profile":
            if self.profile_tag != None:
                if self.profile_tag not in State.profileData:
                    State.profileData[self.profile_tag] = {}
                if self.profile_port != None:
                    if "regular" not in State.profileData[self.profile_tag]:
                        State.profileData[self.profile_tag]["regular"] = {}
                    for ip in data:
                        if ip not in State.profileData[self.profile_tag]["regular"]:
                            State.profileData[self.profile_tag]["regular"][ip] = {}
                        if self.profile_port not in State.profileData[self.profile_tag]["regular"][ip]:
                            State.profileData[self.profile_tag]["regular"][ip][self.profile_port] = {}
                        State.profileData[self.profile_tag]["regular"][ip][self.profile_port][self.module_name] = data[ip]
    
    @staticmethod
    def targets(val):
        out = []
        if val != None and type(val) == str:
            if bool(re.match(r'^([0-9]+\.){3}[0-9]+$',val)):
                out.append(val)
            elif bool(re.match(r'^([0-9]+\.){3}[0-9]+\/[0-9]+$',val)):
                for addr in netaddr.IPNetwork(val):
                    out.append(str(addr))
            elif bool(re.match(r'^((([0-9]+\.){3}[0-9]+\,)+)(([0-9]+\.){3}[0-9]+)$',val)):
                out.extend(val.split(","))
        return out
