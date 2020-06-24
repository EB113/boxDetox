import socket,threading
import netaddr,os,re
import time,traceback

from src.miscellaneous.config import bcolors,Config
from src.module.portscan.portscanner import PortScanner
from src.menus.commons import State
from src.parsers.nmap_xml import parse_xml,parseNmapData,parseNmapPort

def target(val=None):
	if val is None:
		return False
	elif bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val)):
		return True
	return False

def port(val=None):
	if val is None:
		return False
	elif bool(re.match(r"^[0-9]{1,5}$",val)) and int(val) < 65536:
		return True
	return False

def outfile():
	return True

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

class Module_SCAN_TCPCommon(PortScanner):

	#opt = {"target":target}#,"outfile":outfile}#{"target":target,"output":flag}
	opt_static = {"target":target} # REQUIRED
	opt_dynamic = {"maxport":port,"minport":port} # OPTIONAL

	def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

	def getPorts(tag,ip):
		data = State.profileData[tag]["portscan"][Module_SCAN_TCPCommon.getName()][ip]
		return parseNmapPort(data)

	def getName():
		return "Module_SCAN_TCPCommon"

	def printData(data=None,conn=None):
		if data != None and type(data) == list and len(data)>0:
			if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True" and conn != None:
				parsed_data = parseNmapData(data)
				conn.sendall((bcolors.OKBLUE+bcolors.BOLD+parsed_data+bcolors.ENDC+"\n").encode())
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				parsed_data = parseNmapData(data)
				print("{}{}{}{}".format(bcolors.OKBLUE,bcolors.BOLD,parsed_data,bcolors.ENDC))
	
	# Validating user module options
	def validate(opt_dict=None):
		valid = True
		opt = dict(Module_SCAN_TCPCommon.opt_static)
		if opt_dict != None and len(opt_dict.keys()) >= len(Module_SCAN_TCPCommon.opt_static.keys()):
			for k,v in opt_dict.items():
				if k in Module_SCAN_TCPCommon.opt_static:
					valid = valid and Module_SCAN_TCPCommon.opt_static.get(k,None)(v)
					try:
						opt.pop(k, None)
					except:
						print("{}".format(e))
						print("{}".format(traceback.print_exc()))
						return False
				elif k in Module_SCAN_TCPCommon.opt_dynamic:
					valid = valid and Module_SCAN_TCPCommon.opt_dynamic.get(k,None)(v)
		
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
		
	def run(self):
		try:
			lst = Module_SCAN_TCPCommon.targets(self.opt_dict["target"])
			fn = Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID']+"/portscans/"
			data = {}
			for ip in lst:
				try:
					if not os.path.isdir(fn+ip):
						os.mkdir(fn+ip)
					if "minport" in self.opt_dict:
						if "maxport" in self.opt_dict:
							os.system("nmap -p "+self.opt_dict["minport"]+"-"+self.opt_dict["maxport"]+" -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")
						else:						
							os.system("nmap -p "+self.opt_dict["minport"]+"-65535 -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")
					elif "maxport" in self.opt_dict:
						os.system("nmap -p 0-"+self.opt_dict["maxport"]+" -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")
					else:
						os.system("nmap -p- -sT -sV -T4 "+ip+" -oA "+fn+ip+"/tcp_"+ip+" 1>/dev/null 2>/dev/null")

					nmap_data = parse_xml(fn+ip+"/tcp_"+ip+".xml")
				except Exception as e:
					print("{}".format(e))
					print("{}".format(traceback.print_exc()))

				data[ip] = nmap_data

			self.storeDataPortscan(data)
			if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
					s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
					try:
						for val in data.values():
							Module_SCAN_TCPCommon.printData(val,s)
					finally:
						s.close()
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				for val in data.values():
					Module_SCAN_TCPCommon.printData(val)

		except Exception as e:
			print("{}".format(e))
			print("{}".format(traceback.print_exc()))
		return
