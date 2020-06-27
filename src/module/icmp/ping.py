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

	def run(self):
		lst = self.targets(self.opt_dict["target"])
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
