import threading
import netaddr,os,re

from src.miscellaneous.config import bcolors
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

class Module_Ping(Module):

	opt = {"target":target}#{"target":target,"output":flag}

	def __init__(self,opt_dict):
		threading.Thread.__init__(self)
		super().__init__()
		self.opt_dict = opt_dict

	# Validating user module options
	def validate(opt_dict):
		valid = True
		if len(opt_dict.keys()) == len(Module_Ping.opt.keys()):
			for k,v in opt_dict.items():
				valid = valid and Module_Ping.opt.get(k,None)(v)
		else:
			valid = False
		return valid
		
	def targets(self,val=None):
		out = []
		if bool(re.match(r'^([0-9]+\.){3}[0-9]+$',val)):
			out.append(val)
		elif bool(re.match(r'^([0-9]+\.){3}[0-9]+\/[0-9]+$',val)):
			for addr in netaddr.IPNetwork(val):
				out.append(str(addr))
		return out

	def run(self):
		lst = self.targets(self.opt_dict["target"])
		for ip in lst:
			if not self.flag.is_set():
				proc = os.popen("ping -c 1 " + ip)
				out = proc.read()
				proc.close()
				if "bytes from" in out:
					print("{}[*]{} {}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,ip))
		return
