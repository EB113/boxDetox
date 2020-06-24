import threading,socket
import netaddr,os,subprocess,re

from src.miscellaneous.config import Config,bcolors
from src.module.module import Module

import time

def target(val=None):
	if val is None:
		return False
	else:
		return bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val))

def port(val=None):
	if val is None:
		return False
	else:
		try:
			int(val)
			return True
		except:
			return False

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_SMTP_nmapenum(Module):

	opt_static = {"target":target,"port":port}#{"target":target,"output":flag}
	opt_dynamic = {}#{"target":target,"output":flag}

	def __init__(self,opt_dict,mode,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,mode,module_name,profile_tag,profile_port)

	# Validating user module options
	def validate(opt_dict=None):
		valid = True
		opt = dict(Module_SMTP_nmapenum.opt_static)
		if opt_dict != None and len(opt_dict.keys()) >= len(Module_SMTP_nmapenum.opt_static.keys()):
			for k,v in opt_dict.items():
				if k in Module_SMTP_nmapenum.opt_static:
					valid = valid and Module_SMTP_nmapenum.opt_static.get(k,None)(v)
					try:
						opt.pop(k, None)
					except:
						print("{}".format(e))
						print("{}".format(traceback.print_exc()))
						return False
				elif k in Module_SMTP_nmapenum.opt_dynamic:
					valid = valid and Module_SMTP_nmapenum.opt_dynamic.get(k,None)(v)
		
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
		return "Module_SMTP_nmapenum"
	
	def printData(data=None,conn=None):
		if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
			conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode())	
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,data,bcolors.ENDC))

	def run(self):
		lst = Module_SMTP_nmapenum.targets(self.opt_dict["target"])
		data = {}
		for ip in lst:
			if not self.flag.is_set():
				proc = os.popen("/bin/bash -c 'nmap -p "+ self.opt_dict["port"] +" --script=smtp-enum* "+ip+"'")
				out = proc.read()
				proc.close()
				if self.mode == "profile": 
					fd = open(Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID']+"/profile/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/nmap_enum","w")
					fd.write(out)
					fd.close()
				data[ip] = out
				self.storeDataRegular(data)
				if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
						s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
						try:
							s.sendall((bcolors.BOLD+out+bcolors.ENDC).encode())	
						finally:
							s.close()
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					print("{}{}{}".format(bcolors.BOLD,out,bcolors.ENDC))
			else:
				break
		return
