import re,readline,sys,importlib,socket
import time,json

from src.miscellaneous.completer import Completer
from src.miscellaneous.config import bcolors, Config
from src.profile.profiler	import Profiler
from src.module.monitor		import Monitor

from src.menus.commons import State
from src.menus.bof import bof_badchars,bof_pattern,bof_offset,bof_lendian,bof_nasm,bof_nops,bof_notes
from src.menus.module import module_run,module_get,module_set,switcher_module
from src.menus.external import external_edit,external_use,external_search,external_shellz
from src.menus.internal import *

from src.parsers.nmap_xml import *

# Export Session Config Values to JSON
def configExport(pathOUT):
	try:
		cfg = {}
		members = [attr for attr in dir(Config) if not callable(getattr(Config, attr)) and not attr.startswith("__")]
		for member in members:
			cfg[member] = getattr(Config,member)
		fd = open(pathOUT,"w")
		fd.write(json.dumps(cfg))
		fd.close()
	except Exception as e:
		print("{}".format(e))
		print("{}".format(traceback.print_exc()))	
		print("{}Error exporting config.json file! File path:{}{}".format(bcolors.WARNING,pathOUT,bcolors.ENDC))
		pass

# Import JSON values to Config
def configImport(pathIN):
	try:
		fd = open(pathIN,"r")
		cfg = json.loads(fd.read())
		fd.close()
		for k,v in cfg.items():
			setattr(Config,k,v)
	except Exception as e:
		print("{}".format(e))
		print("{}".format(traceback.print_exc()))	
		print("{}Error importing config.json file! File path:{}{}".format(bcolors.WARNING,pathIN,bcolors.ENDC))
		pass

# Export Session State.moduleData Values to JSON
def moduleExport(pathOUT):
	try:
		fd = open(pathOUT,"w")
		fd.write(json.dumps(State.moduleData))
		fd.close()
	except Exception as e:
		print("{}".format(e))
		print("{}".format(traceback.print_exc()))	
		print("{}Error exporting module.json file! File path:{}{}".format(bcolors.WARNING,pathOUT,bcolors.ENDC))
		pass
# Import JSON values to State.moduleData
def moduleImport(pathIN):
	try:
		fd = open(pathIN,"r")
		State.moduleData = json.loads(fd.read())
		fd.close()
	except Exception as e:
		print("{}".format(e))
		print("{}".format(traceback.print_exc()))	
		print("{}Error importing module.json file! File path:{}{}".format(bcolors.WARNING,pathIN,bcolors.ENDC))
		pass

# Export Session State.profileData Values to JSON
def profileExport(pathOUT):
	try:
		fd = open(pathOUT,"w")
		fd.write(json.dumps(State.profileData))
		fd.close()
	except Exception as e:
		print("{}".format(e))
		print("{}".format(traceback.print_exc()))	
		print("{}Error exporting profile.json file! File path:{}{}".format(bcolors.WARNING,pathOUT,bcolors.ENDC))
		pass
# Import JSON values to State.profileData
def profileImport(pathIN):
	try:
		fd = open(pathIN,"r")
		State.profileData = json.loads(fd.read())
		fd.close()
	except Exception as e:
		print("{}".format(e))
		print("{}".format(traceback.print_exc()))	
		print("{}Error importing profile.json file! File path:{}{}".format(bcolors.WARNING,pathIN,bcolors.ENDC))
		pass

def save(cmd=None):
	session = ""
	if len(cmd) == 2:
		session = cmd[1]
	elif len(cmd) == 1:
		session = Config.CONFIG['GENERAL']['SESSID']
	else:
		print("{}Usage: save <empty||session_name>{}".format(bcolors.WARNING,bcolors.ENDC))
		return

	configExport(Config.CONFIG['GENERAL']['PATH']+"/db/sessions/"+session+"/config.json")
	moduleExport(Config.CONFIG['GENERAL']['PATH']+"/db/sessions/"+session+"/module.json")
	profileExport(Config.CONFIG['GENERAL']['PATH']+"/db/sessions/"+session+"/profile.json")

def load(cmd=None):
	if len(cmd) == 2:
		path = Config.CONFIG['GENERAL']['PATH']+"/db/sessions/"+cmd[1]
		if os.path.isdir(path) and os.path.isfile(path+"/config.json") and os.path.isfile(path+"/module.json") and os.path.isfile(path+"/profile.json"):
			configImport(path+"/config.json")
			moduleImport(path+"/module.json")
			profileImport(path+"/profile.json")
		else:
			print("{}Session not found!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: load <session_name>{}".format(bcolors.WARNING,bcolors.ENDC))


def getKey(dictionary,val):
	for k,v in dictionary.items():
		if v == val:
			return k
	return None

def config(cmd=None):

	if len(cmd) == 2 and cmd[1] == "get":
		for k1,v1 in Config.CONFIG.items():
			print("{}{}{}:{}".format(bcolors.BOLD,bcolors.WARNING,k1,bcolors.ENDC))
			for k2,v2 in v1.items():
				print("{}[*] {} -> {}{}".format(bcolors.OKBLUE,k2,v2,bcolors.ENDC))

	elif len(cmd) == 3 and cmd[1] == "get":
		found = False
		for k1,v1 in Config.CONFIG.items():
			for k2,v2 in v1.items():
				if cmd[2] == k2:
					found = True
					print("{}[*] {} -> {}{}".format(bcolors.OKBLUE,k2,v2,bcolors.ENDC))
		if not found:
			print("{}Config value not found!{}".format(bcolors.WARNING,bcolors.ENDC))
	elif len(cmd) == 4 and cmd[1] == "set":
		found = False
		for k1,v1 in Config.CONFIG.items():
			for k2,v2 in v1.items():
				if cmd[2] == k2:
					found = True
					Config.CONFIG[k1][k2] = cmd[3]
		if not found:
			print("{}Config value not found!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: config <get <empty||{{option}}>|set {{option}} {{value}}>{}".format(bcolors.WARNING,bcolors.ENDC))

def profile(cmd=None):
	filters = ["tag","name","ip","port","type"]
	if len(cmd) == 2 and cmd[1] == "help":
		print("Filters: {}".format(filters))
		print("{}Usage: profile <e.g:profile=prof ip=127.0.0.1||help||clear>{}".format(bcolors.OKBLUE,bcolors.ENDC))
		return
	elif len(cmd) == 2 and cmd[1] == "clear":
		State.profileData = {}
		print("{}Profile data cleared!{}".format(bcolors.OKBLUE,bcolors.ENDC))
		return

	filters_valid = {}
	for filt in cmd[1:]:
		if re.match("^[a-z]+\=[a-zA-Z0-9._-]+$",filt):
			filt_split = filt.split("=")
			if filt_split[0] in filters:
				filters_valid[filt_split[0]]=filt_split[1]


	s = None
	if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
	try:
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
			print("{}{}Profile Data{}".format(bcolors.BOLD,bcolors.WARNING,bcolors.ENDC))
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
			s.sendall((bcolors.BOLD+bcolors.WARNING+"Profile Data"+bcolors.ENDC+"\n").encode())
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())

		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "portscan"):
		
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
				print("{}{}Type:{} {}{}Portscan{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,bcolors.OKBLUE,bcolors.ENDC))
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
			if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.BOLD+bcolors.FAIL+"Type: "+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+"Portscan"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
			
			for tag,type_list in State.profileData.items():
				if "tag" in filters_valid and filters_valid["tag"] != t:
					continue
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
					print("{}{}Tag:{} {}{}{}{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,bcolors.OKBLUE,tag,bcolors.ENDC))
					print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
				if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.BOLD+bcolors.FAIL+"Tag:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" "+tag+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
				
				if "portscan" in type_list:
					for mod,ip_list in type_list["portscan"].items():
						if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
							print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,mod,bcolors.ENDC))
							print("{}{}Name: {}{}".format(bcolors.BOLD,bcolors.OKGREEN,mod,bcolors.ENDC))
							print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,mod,bcolors.ENDC))
						if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
							s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
							s.sendall((bcolors.BOLD+bcolors.OKGREEN+"Name:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" "+mod+bcolors.ENDC+"\n").encode())
							s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
		
						for ip,data in ip_list.items():
							if "ip" in filters_valid and filters_valid["ip"] != ip:
								continue
							module_path = getKey(switcher_module,mod)
							if module_path != None:
								module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),mod)
								module_class.printData(data,s)
		
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())


		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "regular"):
		
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
				print("{}{}Type:{} {}{}Regular{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,bcolors.OKBLUE,bcolors.ENDC))
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
			if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.BOLD+bcolors.FAIL+"Type:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" Regular"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
			
			
			for tag,type_list in State.profileData.items():
				if "tag" in filters_valid and filters_valid["tag"] != t:
					continue
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
					print("{}{}Tag:{} {}{}{}{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,bcolors.OKBLUE,tag,bcolors.ENDC))
					print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
				if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.BOLD+bcolors.FAIL+"Tag:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" "+tag+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
				
				if "regular" in type_list:	
					for ip,port_list in type_list["regular"].items():
						if "ip" in filters_valid and filters_valid["ip"] != ip:
							continue
						#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
						for port,mod_list in port_list.items():
							if "port" in filters_valid and filters_valid["port"] != port:
								continue
							for mod,data in mod_list.items():
								if "name" in filters_valid and filters_valid["name"] != mod:
									continue
							
								if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
									print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,bcolors.ENDC))
									print("{}{}Name: {}{}".format(bcolors.BOLD,bcolors.OKGREEN,mod,bcolors.ENDC))
									print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,bcolors.ENDC))
								if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
									s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
									s.sendall((bcolors.BOLD+bcolors.OKGREEN+"Name:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" "+mod+bcolors.ENDC+"\n").encode())
									s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
							
								module_path = getKey(switcher_module,mod)
								if module_path != None:
									module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),mod)
									module_class.printData(data,s)
		
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}----------------------------------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.WARNING+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()

def module(cmd=None):
	filters = ["name","ip","type"]
	if len(cmd) == 2 and cmd[1] == "help":
		print("Filters: {}".format(filters))
		print("{}Usage: module <e.g:name=Module_Ping ip=127.0.0.1||help||clear>{}".format(bcolors.OKBLUE,bcolors.ENDC))
		return
	elif len(cmd) == 2 and cmd[1] == "clear":
		State.moduleData = {"portscan":{},"regular":{}}
		print("{}Module data cleared!{}".format(bcolors.OKBLUE,bcolors.ENDC))
		return

	filters_valid = {}
	for filt in cmd[1:]:
		if re.match("^[a-z]+\=[a-zA-Z0-9._-]+$",filt):
			filt_split = filt.split("=")
			if filt_split[0] in filters:
				filters_valid[filt_split[0]]=filt_split[1]
	s = None
	if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
	try:
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
			print("{}Modules Data{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
			s.sendall((bcolors.WARNING+"Modules Data"+bcolors.ENDC+"\n").encode())
	
		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "portscan"):
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
				print("{}{}Type:{} {}{}Portscan{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,bcolors.OKBLUE,bcolors.ENDC))
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
			if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.BOLD+bcolors.FAIL+"Type: "+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+"Portscan"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
			
			for m,d in State.moduleData["portscan"].items():
				if "name" in filters_valid and filters_valid["name"] != m:
					continue
				
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,mod,bcolors.ENDC))
					print("{}{}Name: {}{}".format(bcolors.BOLD,bcolors.OKGREEN,mod,bcolors.ENDC))
					print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,mod,bcolors.ENDC))
				if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.BOLD+bcolors.OKGREEN+"Name:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" "+mod+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
				
				for ip,v in d.items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					module_path = getKey(switcher_module,m)
					if module_path != None:
						module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),m)
						module_class.printData(v,s)
		

		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())


		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())
				
		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "regular"):
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
				print("{}{}Type:{} {}{}Regular{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC,bcolors.BOLD,bcolors.OKBLUE,bcolors.ENDC))
				print("{}------------------------------------{}".format(bcolors.FAIL,bcolors.ENDC))
			if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.BOLD+bcolors.FAIL+"Type:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" Regular"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.FAIL+"------------------------------------"+bcolors.ENDC+"\n").encode())
			
			for m,d in State.moduleData["regular"].items():
				if "name" in filters_valid and filters_valid["name"] != m:
					continue
				
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,mod,bcolors.ENDC))
					print("{}{}Name: {}{}".format(bcolors.BOLD,bcolors.OKGREEN,mod,bcolors.ENDC))
					print("{}----------------------------------------------------------------{}".format(bcolors.OKGREEN,mod,bcolors.ENDC))
				if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.BOLD+bcolors.OKGREEN+"Name:"+bcolors.ENDC+bcolors.BOLD+bcolors.OKBLUE+" "+mod+bcolors.ENDC+"\n").encode())
					s.sendall((bcolors.OKGREEN+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
				
				for ip,v in d.items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					module_path = getKey(switcher_module,m)
					if module_path != None:
						module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),m)
						module_class.printData(v,s)
		
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}----------------------------------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.WARNING+"----------------------------------------------------------------"+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()


def services(cmd=None):
	filters = ["type","module","profile","ip"]
	if len(cmd) == 2 and cmd[1] == "help":
		print("Filters: {}".format(filters))
		print("{}Usage: services <e.g:profile=prof ip=127.0.0.1||help>{}".format(bcolors.OKBLUE,bcolors.ENDC))
		return

	filters_valid = {}
	for filt in cmd[1:]:
		if re.match("^[a-z]+\=[a-zA-Z0-9._-]+$",filt):
			filt_split = filt.split("=")
			if filt_split[0] in filters:
				filters_valid[filt_split[0]]=filt_split[1]

	s = None
	if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
	try:
		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "module"):
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
				print("{}Modules Data{}".format(bcolors.WARNING,bcolors.ENDC))
			if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.WARNING+"Modules Data"+bcolors.ENDC+"\n").encode())
		
			for m,d in State.moduleData["portscan"].items():
				if "name" in filters_valid and filters_valid["name"] != m:
					continue
				
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					print("{}Name: {}{}".format(bcolors.OKBLUE,m,bcolors.ENDC))
				if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					s.sendall((bcolors.OKBLUE+"Name: "+m+bcolors.ENDC+"\n").encode())
				
				for ip,v in d.items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					module_path = getKey(switcher_module,m)
					if module_path != None:
						module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),m)
						module_class.printData(v,s)
		
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())

		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "profile"):
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
				print("{}Profiles Data{}".format(bcolors.WARNING,bcolors.ENDC))
			if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.WARNING+"Profiles Data"+bcolors.ENDC+"\n").encode())
			
			for tag,type_list in State.profileData.items():
				if "profile" in filters_valid and filters_valid["profile"] != t:
					continue
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					print("{}Tag: {}{}".format(bcolors.OKBLUE,tag,bcolors.ENDC))
				if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					s.sendall((bcolors.OKBLUE+"Tag: "+tag+bcolors.ENDC+"\n").encode())
				
				for mod,ip_list in type_list["portscan"].items():
					if "module" in filters_valid and filters_valid["module"] != t:
						continue
					if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
						print("{}Name: {}{}".format(bcolors.OKBLUE,mod,bcolors.ENDC))
					if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
						s.sendall((bcolors.OKBLUE+"Name: "+mod+bcolors.ENDC+"\n").encode())
		
					for ip,data in ip_list.items():
						if "ip" in filters_valid and filters_valid["ip"] != ip:
							continue
						module_path = getKey(switcher_module,mod)
						if module_path != None:
							module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),mod)
							module_class.printData(data,s)

		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()

def hosts(cmd=None):
	filters = ["module","profile"]
	if len(cmd) == 2 and cmd[1] == "help":
		print("Filters: {}".format(filters))
		print("{}Usage: hosts <e.g:profile=prof port=80||help>{}".format(bcolors.OKBLUE,bcolors.ENDC))
		return

	filters_valid = {}
	for filt in cmd[1:]:
		if re.match("^[a-z]+\=[a-zA-Z0-9._-]+$",filt):
			filt_split = filt.split("=")
			if filt_split[0] in filters:
				filters_valid[filt_split[0]]=filt_split[1]
	hosts_array = []

	if "portscan" in State.moduleData:
		for m,d in State.moduleData["portscan"].items():
			for ip in d:
	   			if ip not in hosts_array:
   					hosts_array.append(ip)
	if "regular" in State.moduleData:
		for m,d in State.moduleData["regular"].items():
			for ip in d:
				if ip not in hosts_array:
					hosts_array.append(ip)
	for tag,type_list in State.profileData.items():
		if "portscan" in type_list:
			for mod,ip_list in type_list["portscan"].items():
				for ip,data in ip_list.items():
					if ip not in hosts_array:
						hosts_array.append(ip)
		if "regular" in type_list:
			for ip in type_list["regular"]:
				if ip not in hosts_array:
					hosts_array.append(ip)

	s = None
	if Config.CONFIG['LOGGER']['LOGGERSTATUS'] == "True" and Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
	try:
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
			print("{}Hosts Data{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
			s.sendall((bcolors.WARNING+"Hosts Data"+bcolors.ENDC+"\n").encode())
		
		for host in hosts_array:
			if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
				print("{}[*]{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,host,bcolors.ENDC))
			if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
				s.sendall((bcolors.OKBLUE+"[*]"+bcolors.ENDC+" "+bcolors.BOLD+host+bcolors.ENDC+"\n").encode())
		
		if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()

def get_options(d,options,id=False):
	global state

	for k,v in d.items():
		if id == True:
			options.append(k)
		elif k == State.menu_state:
			options = get_options(v,options,True)
		elif isinstance(v, dict):
			options = get_options(v,options)
	return options

def help(cmd=None):
	if len(cmd) == 1:
		print("{}Global Command List:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in State.global_option:
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
	elif len(cmd) == 2:
		print("{}ToDo{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: help <empty||cmd>{}".format(bcolors.WARNING,bcolors.ENDC))

def ls(cmd=None):
	if len(cmd) == 1:
		print("{}Menu Command List:{}".format(bcolors.WARNING,bcolors.ENDC))
		options = []
		if State.module_state == "":
			options = get_options(State.menu_option,[])
		else:
			options = State.module_option
		for option in options:
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
	else:
		print("{}Usage: ls{}".format(bcolors.WARNING,bcolors.ENDC))


def switch(cmd=None):
	global completer
	
	State.menu_state = cmd[0]
	del State.actual_option[:]
	if cmd[0]=="external":
		State.actual_option = get_options(State.menu_option,[])+State.global_option+State.config_option+list(switcher_module.keys())
	else:
		State.actual_option = get_options(State.menu_option,[])+State.global_option+State.config_option

def exit(cmd=None):
	if len(cmd) == 1:
		State.menu_state = "exit"
	else:
		print("{}Usage: exit{}".format(bcolors.WARNING,bcolors.ENDC))


def invalid(cmds=None):
	print("{}Invalid Command! Use help/ls for options.{}".format(bcolors.WARNING,bcolors.ENDC))

def get_parent(d,t):
	out = t
	for k,v in d.items():
		if k == State.menu_state:
			return ("",True)
		elif isinstance(v, dict) and len(v) > 0 and out[1] != True:
			tmp = get_parent(v,t)
			if tmp[0] == "" and tmp[1]:
				out = (k,True)
			else:
				out = tmp
	return out

def back(cmd=None):
	global completer

	if len(cmd) == 1:
		del State.actual_option[:]
		if State.module_state == "":
			State.menu_state = get_parent(State.menu_option,("",False))[0]
			State.actual_option = get_options(State.menu_option,[])+State.global_option+State.config_option
		else:
			State.env_option = {}
			State.module_class = ""
			State.module_state = ""
			State.actual_option = get_options(State.menu_option,[])+State.global_option+State.config_option
	else:
		print("{}Usage: back{}".format(bcolors.WARNING,bcolors.ENDC))


def parse(cmd):
	if cmd == "":
		if State.module_state != "":
			return State.module_state
		else:
			return State.menu_state
	if not (cmd is None):
		values = cmd.split()

		if State.module_state == "":
			switcher_menu[State.menu_state].get(values[0], invalid)(values)
			completer.update(State.actual_option)
			if State.module_state != "":
				return State.module_state
			return State.menu_state
		else:
			switcher_menu["module"].get(values[0], invalid)(values)
			completer.update([x for x in State.module_option.keys()]+State.global_option+State.config_option)
			if State.module_state == "":
				return State.menu_state
			return State.module_state
	else:
		return "exit"

# OPTION VALUES
#state = State()
switcher_menu = {"main":{"exit":exit,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"module":module,"profile":profile,"load":load,"save":save,"bof":switch,"external":switch,"shares":switch},"bof":{"badchars":bof_badchars,"pattern":bof_pattern,"offset":bof_offset,"lendian":bof_lendian,"nasm":bof_nasm,"nops":bof_nops,"notes":bof_notes,"exit":exit,"help":help,"ls":ls,"back":back,"config":config,"hosts":hosts,"services":services,"module":module,"profile":profile,"load":load,"save":save},"external":{"shellZ":switch,"edit":external_edit,"use":external_use,"search":external_search,"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"module":module,"profile":profile,"load":load,"save":save},"module":{"go":module_run,"get":module_get,"set":module_set,"exit":exit,"help":help,"ls":ls,"back":back,"config":config,"hosts":hosts,"services":services,"module":module,"profile":profile,"load":load,"save":save},"shares":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"module":module,"profile":profile,"load":load,"save":save,"smb":internal_share,"ftp":internal_share,"http":internal_share,"powershell":internal_share,"vbscript":internal_share},"shellZ":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"services":services,"module":module,"profile":profile,"hosts":hosts,"load":load,"save":save,"linux_x86":external_shellz,"windows_x86":external_shellz,"php":external_shellz,"asp":external_shellz,"jsp":external_shellz,"notes":external_shellz}}

# AUTOCOMPLETE SETUP
completer = Completer(get_options(State.menu_option,[])+State.global_option+State.config_option)
delims = readline.get_completer_delims()
readline.set_completer_delims(delims.replace("/",""))
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

# PROCESS MONITOR
watchdog = Monitor(State.procs)
watchdog.start()
