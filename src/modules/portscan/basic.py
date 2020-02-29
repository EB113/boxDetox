import threading
import netaddr,os,re
import time

from src.miscellaneous.config import bcolors,Config
from src.modules.portscan.portscanner import PortScanner
from src.parsers.nmap_xml import *

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

	def __init__(self,opt_dict,save_location):
		threading.Thread.__init__(self)
		super().__init__()
		self.opt_dict = opt_dict

	def getPorts(data=None):
		return ["80","443"]

	def printData(data=None):
		if data != None and type(data) = dict and len(data)>0:
			for ip,v in data.items():
			print(data)
	
	def storeData(self,data=None):
		print(data)
	
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
		lst = Module_TCPCommon.targets(self.opt_dict)
		fn = Config.PATH+"/db/sessions/"+Config.SESSID+"/tmp.xml"
		self.data = {}
		for ip in lst:
			fn = Config.PATH+
			os.system("nmap -sT -sV -T4 "+ip+" -oX "+fn)
			data = nmap_xml.parse_xml(fn)
			self.data[ip] = data

		return
