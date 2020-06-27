import socket,threading
import netaddr,os,re
import time,traceback

from src.miscellaneous.config import bcolors,Config
from src.module.portscan.portscanner import PortScanner
from src.parsers.nmap_xml import parse_xml

def target(val=None):
    if val is None:
        return False
    elif bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val)):
        return True
    return False

def port(val=None):
    if val is None:
        return False
    elif bool(re.match(r"^[0-9]{1,5}$",val)) and int(val) < 65536:
        return True
    return False

def outfile():
    return True

#Need to see how to deal with multiple flags
def flag(val=None):
    return True

class Module_SCAN_TCP(PortScanner):

    #opt = {"target":target}#,"outfile":outfile}#{"target":target,"output":flag}
    opt_static = {"target":target} # REQUIRED
    opt_dynamic = {"maxport":port,"minport":port} # OPTIONAL

    def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
        threading.Thread.__init__(self)
        super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

    def run(self):
        try:
            lst = Module_SCAN_TCP.targets(self.opt_dict["target"])
            fn = Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID']+"/portscans/"
            data = {}
            for ip in lst:
                try:
                    if not os.path.isdir(fn+ip):
                        os.mkdir(fn+ip)
                    if "minport" in self.opt_dict:
                        if "maxport" in self.opt_dict:
                            os.system("nmap -p "+self.opt_dict["minport"]+"-"+self.opt_dict["maxport"]+" -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")
                        else:                       
                            os.system("nmap -p "+self.opt_dict["minport"]+"-65535 -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")
                    elif "maxport" in self.opt_dict:
                        os.system("nmap -p 0-"+self.opt_dict["maxport"]+" -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")
                    else:
                        os.system("nmap -p- -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")

                    nmap_data = parse_xml(fn+ip+"/tcp_"+ip+".xml")
                except Exception as e:
                    print("{}".format(e))
                    print("{}".format(traceback.print_exc()))

                data[ip] = nmap_data

            self.storeDataPortscan(data)
            if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
                    try:
                        for val in data.values():
                            self.printData(val,s,True)
                    finally:
                        s.close()
            if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
                for val in data.values():
                    self.printData(val,enclose=True)

        except Exception as e:
            print("{}".format(e))
            print("{}".format(traceback.print_exc()))
        return
