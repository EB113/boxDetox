import socket,threading
import netaddr,os,re
import time,traceback

from src.miscellaneous.config import bcolors,Config
from src.modules.portscan.portscanner import PortScanner
from src.menus.commons import State
from src.parsers.nmap_xml import parse_xml,parseNmapData,parseNmapPort

def target(val=None):
	if val is None:
		return False
	else:
#Check if file or ip
		return bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val))

def outfile():
	return True

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_TCPCommon(PortScanner):

	opt = {"target":target}#,"outfile":outfile}#{"target":target,"output":flag}

	def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

	def getPorts(tag,ip):
		data = State.profileData[tag]["portscan"][Module_TCPCommon.getName()][ip]
		return parseNmapPort(data)

	def getName():
		return "Module_TCPCommon"

	def printData(data=None,conn=None):
		if data != None and type(data) == list and len(data)>0:
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True" and conn != None:
				parsed_data = parseNmapData(data)
				conn.sendall((bcolors.OKBLUE+bcolors.BOLD+parsed_data+bcolors.ENDC+"\n").encode())
			if Config.CLIENTVERBOSE == "True":
				parsed_data = parseNmapData(data)
				print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,parsed_data,bcolors.ENDC))
	
	# Validating user module options
	def validate(opt_dict):
		valid = True
		if len(opt_dict.keys()) == len(Module_TCPCommon.opt.keys()):
			for k,v in opt_dict.items():
				valid = valid and Module_TCPCommon.opt.get(k,None)(v)
		else:
			valid = False
		return valid
		
	def run(self):
		try:
			lst = Module_TCPCommon.targets(self.opt_dict["target"])
			fn = Config.PATH+"/db/sessions/"+Config.SESSID+"/tmp.xml"
			data = {}
			for ip in lst:
				try:
					os.system("nmap -sT -sV -T4 "+ip+" -oX "+fn+" 1>/dev/null")
					nmap_data = parse_xml(fn)
				except Exception as e:
					print("{}".format(e))
					print("{}".format(traceback.print_exc()))

				data[ip] = nmap_data
			self.storeDataPortscan(data)
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
					s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
					try:
						for val in data.values():
							Module_TCPCommon.printData(val,s)
					finally:
						s.close()
			if Config.CLIENTVERBOSE == "True":
				for val in data.values():
					Module_TCPCommon.printData(val)

		except Exception as e:
			print("{}".format(e))
			print("{}".format(traceback.print_exc()))
		return
