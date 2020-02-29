import threading,socket
import netaddr,os,re

from src.miscellaneous.config import Config,bcolors
from src.modules.module import Module
from src.menus.commons import State

import time

def target(val=None):
	if val is None:
		return False
	else:
		return bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val))

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_Ping(Module):

	opt = {"target":target}#{"target":target,"output":flag}

	def __init__(self,opt_dict,save_location,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__()
		self.opt_dict = opt_dict
		self.save_location = save_location
		self.profile_tag = profile_tag
		self.profile_port = profile_port

	# Validating user module options
	def validate(opt_dict):
		valid = True
		if len(opt_dict.keys()) == len(Module_Ping.opt.keys()):
			for k,v in opt_dict.items():
				valid = valid and Module_Ping.opt.get(k,None)(v)
		else:
			valid = False
		return valid
	
	def printData(data=None):
		print(data)

	def storeData(self):
		if self.save_location == "module":
			if "regular" not in State.moduleData:
				State.moduleData["regular"] = {}
			if "Module_Ping" not in State.moduleData["regular"]:
				State.moduleData["regular"]["Module_Ping"] = {}
			for ip in self.data:
				State.moduleData["regular"]["Module_Ping"][ip] = self.data[ip]
		elif self.save_location == "profile":
			if self.profile_tag != None:
				if self.profile_tag not in State.profileData:
					State.profileData[self.profile_tag] = {}
				if self.profile_port != None:
					if "regular" not in State.moduleData[self.profile_tag]:
						State.moduleData[self.profile_tag]["regular"] = {}
					for ip in self.data:
						if ip not in State.profileData[self.profile_tag]["regular"]:
							State.profileData[self.profile_tag]["regular"][ip] = {}
						if self.profile_port not in State.profileData[self.profile_tag]["regular"][ip]:
							State.profileData[self.profile_tag]["regular"][ip][self.profile_port] = {}
						State.profileData[self.profile_tag]["regular"][ip][self.profile_port]["Module_Ping"] = self.data[ip]

	def run(self):
		lst = Module_Ping.targets(self.opt_dict["target"])
		self.data = {}
		for ip in lst:
			if not self.flag.is_set():
				proc = os.popen("ping -c 1 " + ip)
				out = proc.read()
				proc.close()
				if "bytes from" in out:
					self.data[ip]=ip
					if Config.VERBOSE == "True":
						if Config.LOGGERSTATUS == "True":
							with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
								s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
								try:
									s.sendall((bcolors.OKBLUE+"[*]"+bcolors.ENDC+" "+bcolors.BOLD+ip+bcolors.ENDC).encode())	
								finally:
									s.close()
						else:
							print("{}[*]{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,ip,bcolors.ENDC))
			else:
				break
		#Store Data for Global query
		self.storeData()
		return
