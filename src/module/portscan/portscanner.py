from src.module.module import Module
from src.menus.commons import State
from src.parsers.nmap_xml import parseNmapPort, parseNmapService, parseNmapPortService, parseNmapData
from src.menus.commons import State
from src.miscellaneous.config import Config,bcolors


class PortScanner(Module):

    def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
        super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

    @classmethod
    def getPorts(cls,tag,ip):
        if cls.__name__ in State.profileData[tag]["portscan"]:
            data = State.profileData[tag]["portscan"][cls.__name__][ip]
            return parseNmapPort(data)
        else:
            return []

    @classmethod
    def getServices(cls,tag,ip):
        if cls.__name__ in State.profileData[tag]["portscan"]:
            data = State.profileData[tag]["portscan"][cls.__name__][ip]
            return parseNmapService(data)
        else:
            return []

    @classmethod
    def getPortsServices(cls,tag,ip):
        if cls.__name__ in State.profileData[tag]["portscan"]:
            data = State.profileData[tag]["portscan"][cls.__name__][ip]
            return parseNmapPortService(data)
        else:
            return []
    
    @classmethod
    def printData(cls,data=None,conn=None,enclose=False):
        if data != None and type(data) == list and len(data)>0:
            if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
                parsed_data = parseNmapData(data)
                if enclose:
                    # Header
                    conn.sendall((bcolors.FAIL+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
                    conn.sendall((bcolors.BOLD+bcolors.FAIL+"Name:"+bcolors.ENDC+bcolors.BOLD+" "+cls.__name__+bcolors.ENDC+"\n").encode())
                # Body
                conn.sendall((bcolors.OKBLUE+bcolors.BOLD+parsed_data+bcolors.ENDC+"\n").encode())
                # Footer
                if enclose:
                    conn.sendall((bcolors.FAIL+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())

            if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
                parsed_data = parseNmapData(data)
                if enclose:
                    # Header
                    print("{}----------------------------------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
                    print("{}{}Name:{} {}{}{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,cls.__name__,bcolors.ENDC))
                # Body
                print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,parsed_data,bcolors.ENDC))
                if enclose:
                    # Footer
                    print("{}----------------------------------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
