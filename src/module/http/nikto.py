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

def secure(val=None):
	if val is None:
		return False
	else:
		return (val == "True" or val == "False")

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_HTTP_nikto(Module):

	opt_static = {"target":target, "secure":secure}#{"target":target,"output":flag}
	opt_dynamic = {}#{"target":target,"output":flag}

	def __init__(self,opt_dict,mode,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,mode,module_name,profile_tag,profile_port)

	# Validating user module options
	def validate(opt_dict=None):
		valid = True
		opt = dict(Module_HTTP_nikto.opt_static)
		if opt_dict != None and len(opt_dict.keys()) >= len(Module_HTTP_nikto.opt_static.keys()):
			for k,v in opt_dict.items():
				if k in Module_HTTP_nikto.opt_static:
					valid = valid and Module_HTTP_nikto.opt_static.get(k,None)(v)
					try:
						opt.pop(k, None)
					except:
						print("{}".format(e))
						print("{}".format(traceback.print_exc()))
						return False
				elif k in Module_HTTP_nikto.opt_dynamic:
					valid = valid and Module_HTTP_nikto.opt_dynamic.get(k,None)(v)
		
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
		return "Module_HTTP_nikto"
	
	def printData(data=None,conn=None):
		if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
			conn.sendall((bcolors.OKBLUE+bcolors.BOLD+data+bcolors.ENDC+"\n").encode())	
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,data,bcolors.ENDC))

	def run(self):
		lst = Module_HTTP_nikto.targets(self.opt_dict["target"])
		data = {}
		for ip in lst:
			if not self.flag.is_set():
				if self.opt_dict["secure"] == "False":
					proc = os.popen("nikto -h  http://" + ip + " 2>/dev/null | grep -E '^\+ .*$' | sed '1,4d' | tac | sed '1,3d' | tac")
				else:
					proc = os.popen("nikto -h  https://" + ip + " 2>/dev/null | grep -E '^\+ .*$' | sed '1,4d' | tac | sed '1,3d' | tac")
				out = proc.read()
				proc.close()
				if self.mode == "profile": 
					fd = open(Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID']+"/profile/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/nikto","w")
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
