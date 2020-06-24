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

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_ICMP_Ping(Module):

	opt_static = {"target":target}#{"target":target,"output":flag}
	opt_dynamic = {}#{"target":target,"output":flag}

	def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

	# Validating user module options
	def validate(opt_dict=None):
		valid = True
		opt = dict(Module_ICMP_Ping.opt_static)
		if opt_dict != None and len(opt_dict.keys()) >= len(Module_ICMP_Ping.opt_static.keys()):
			for k,v in opt_dict.items():
				if k in Module_ICMP_Ping.opt_static:
					valid = valid and Module_ICMP_Ping.opt_static.get(k,None)(v)
					try:
						opt.pop(k, None)
					except:
						print("{}".format(e))
						print("{}".format(traceback.print_exc()))
						return False
				elif k in Module_ICMP_Ping.opt_dynamic:
					valid = valid and Module_ICMP_Ping.opt_dynamic.get(k,None)(v)
		
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
		return "Module_ICMP_Ping"
	
	def printData(data=None,conn=None):
		if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
			conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode())	
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,data,bcolors.ENDC))

	def run(self):
		lst = Module_ICMP_Ping.targets(self.opt_dict["target"])
		time.sleep(25)	
		data = {}
		for ip in lst:
			if not self.flag.is_set():
				proc = os.popen("ping -c 1 " + ip)
				out = proc.read()
				proc.close()
				if "bytes from" in out:
					data[ip]=ip

					if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
						with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
							s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
							try:
								s.sendall((bcolors.OKBLUE+"[*]"+bcolors.ENDC+" "+bcolors.BOLD+ip+bcolors.ENDC).encode())	
							finally:
								s.close()
					if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
						print("{}[*]{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,ip,bcolors.ENDC))
			else:
				break
		#Store Data for Global query
		self.storeDataRegular(data)
		return
