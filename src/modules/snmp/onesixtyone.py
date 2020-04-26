import threading,socket
import netaddr,os,subprocess,re

from src.miscellaneous.config import Config,bcolors
from src.modules.module import Module

import time

def target(val=None):
	if val is None:
		return False
	else:
		return bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val))

def community(val=None):
    if val is None:
        return False
    else:
        return os.path.isfile(val)

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_SNMP_onesixtyone(Module):

	opt = {"target":target,"community":community}#{"target":target,"output":flag}

	def __init__(self,opt_dict,mode,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,mode,module_name,profile_tag,profile_port)

	# Validating user module options
	def validate(opt_dict):
		valid = True
		if len(opt_dict.keys()) == len(Module_SNMP_onesixtyone.opt.keys()):
			for k,v in opt_dict.items():
				valid = valid and Module_SNMP_onesixtyone.opt.get(k,None)(v)
		else:
			valid = False
		return valid
	
	def getName():
		return "Module_SNMP_onesixtyone"
	
	def printData(data=None,conn=None):
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True" and conn != None:
			conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode())	
		if Config.CLIENTVERBOSE == "True":
			print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,data,bcolors.ENDC))

	def run(self):
		lst = Module_SNMP_onesixtyone.targets(self.opt_dict["target"])
		data = {}
		for ip in lst:
			if not self.flag.is_set():
				proc = os.popen("/bin/bash -c 'onesixtyone -c "+self.opt_dict["community"]+" "+ip+"'")
				out = proc.read()
				proc.close()
				if self.mode == "profile": 
					fd = open(Config.PATH+"/db/sessions/"+Config.SESSID+"/profiles/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/onesixtyone","w")
					fd.write(out)
					fd.close()
				data[ip] = out
				self.storeDataRegular(data)
				if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
					with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
						s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
						try:
							s.sendall((bcolors.BOLD+out+bcolors.ENDC).encode())	
						finally:
							s.close()
				if Config.CLIENTVERBOSE == "True":
					print("{}{}{}".format(bcolors.BOLD,out,bcolors.ENDC))
			else:
				break
		return
