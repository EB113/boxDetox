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

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_Ping6(Module):

	opt = {"target":target}#{"target":target,"output":flag}

	def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

	# Validating user module options
	def validate(opt_dict):
		valid = True
		if len(opt_dict.keys()) == len(Module_Ping6.opt.keys()):
			for k,v in opt_dict.items():
				valid = valid and Module_Ping6.opt.get(k,None)(v)
		else:
			valid = False
		return valid
	
	def getName():
		return "Module_Ping6"
	
	def printData(data=None,conn=None):
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True" and conn != None:
			conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode())	
		if Config.CLIENTVERBOSE == "True":
			print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,data,bcolors.ENDC))

	def run(self):
		lst = Module_Ping6.targets(self.opt_dict["target"])
		time.sleep(26)
		data = {}
		for ip in lst:
			if not self.flag.is_set():
				proc = os.popen("ping -c 1 " + ip)
				out = proc.read()
				proc.close()
				if "bytes from" in out:
					data[ip]=ip

					if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
						with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
							s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
							try:
								s.sendall((bcolors.OKBLUE+"[*]"+bcolors.ENDC+" "+bcolors.BOLD+ip+bcolors.ENDC).encode())	
							finally:
								s.close()
					if Config.CLIENTVERBOSE == "True":
						print("{}[*]{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,ip,bcolors.ENDC))
			else:
				break
		#Store Data for Global query
		self.storeDataRegular(data)
		return
