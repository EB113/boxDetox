import re,readline,sys,importlib,socket
import time

from src.miscellaneous.completer import Completer
from src.miscellaneous.config import bcolors, Config
from src.profiles.profiler	import Profiler
from src.modules.monitor		import Monitor

from src.menus.commons import State
from src.menus.bof import bof_badchars,bof_pattern,bof_offset,bof_lendian,bof_nasm,bof_nops,bof_notes
from src.menus.module import module_run,module_get,module_set,switcher_module
from src.menus.external import external_use,external_search,external_shellz
from src.menus.internal import *
from src.menus.buckets import *

from src.parsers.nmap_xml import *


def getKey(dictionary,val):
	for k,v in dictionary.items():
		if v == val:
			return k
	return None

def config(cmd=None,state=None):

	if len(cmd) == 2 and cmd[1] == "get":
		print("{}Configuration:{}".format(bcolors.OKGREEN,bcolors.ENDC))
		members = [attr for attr in dir(Config) if not callable(getattr(Config, attr)) and not attr.startswith("__")]
		for member in members:
			print("{}[*] {} -> {}{}".format(bcolors.OKBLUE,member,getattr(Config,member),bcolors.ENDC))
	elif len(cmd) == 3 and cmd[1] == "get":
		members = [attr for attr in dir(Config) if not callable(getattr(Config, attr)) and not attr.startswith("__")]
		if cmd[2] in members:
			print("{}[*] {} -> {}{}".format(bcolors.OKBLUE,cmd[2],getattr(Config,cmd[2]),bcolors.ENDC))
		else:
			print("{}Config value not found!{}".format(bcolors.WARNING,bcolors.ENDC))
	elif len(cmd) == 4 and cmd[1] == "set":
		members = [attr for attr in dir(Config) if not callable(getattr(Config, attr)) and not attr.startswith("__")]
		if cmd[2] in members:
			setattr(Config,cmd[2],cmd[3])
			print("{}[*] {} -> {}{}".format(bcolors.OKBLUE,cmd[2],getattr(Config,cmd[2]),bcolors.ENDC))
		else:
			print("{}Config value not found!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: config <list|get {{option}}|set {{option}} {{value}}>{}".format(bcolors.WARNING,bcolors.ENDC))

def profiles(cmd=None,state=None):
	filters = ["tag","name","ip","port","type"]
	if len(cmd) == 2 and cmd[1] == "help":
		print("Filters: {}".format(filters))
		print("{}Usage: services <e.g:profile=prof ip=127.0.0.1||help||clear>{}".format(bcolors.OKBLUE,bcolors.ENDC))
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
	if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
	try:
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
			print("{}Profiles Data{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
			s.sendall((bcolors.WARNING+"Profiles Data"+bcolors.ENDC+"\n").encode())

		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "portscan"):
		
			if Config.CLIENTVERBOSE == "True":
				print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
				print("{}Type: Portscan{}".format(bcolors.OKBLUE,bcolors.ENDC))
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.OKBLUE+"Type: Portscan"+bcolors.ENDC+"\n").encode())
			
			for tag,type_list in State.profileData.items():
				if "tag" in filters_valid and filters_valid["tag"] != t:
					continue
				if Config.CLIENTVERBOSE == "True":
					print("{}Tag: {}{}".format(bcolors.OKBLUE,t,bcolors.ENDC))
				if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
					s.sendall((bcolors.OKBLUE+"Tag: "+t+bcolors.ENDC+"\n").encode())
				
				for ip,port_list in type_list["portscan"].items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					for port,mod_list in port_list.items():
						if "port" in filters_valid and filters_valid["port"] != port:
							continue
						for mod,data in mod_list.items():
							if "name" in filters_valid and filters_valid["name"] != mod:
								continue
							
							if Config.CLIENTVERBOSE == "True":
								print("{}Name: {}{}".format(bcolors.OKBLUE,mod,bcolors.ENDC))
							if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
								s.sendall((bcolors.OKBLUE+"Name: "+mod+bcolors.ENDC+"\n").encode())
							
							module_path = getKey(switcher_module,mod)
							if module_path != None:
								module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),mod)
								module_class.printData(data,s)
		
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())


		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "regular"):
		
			if Config.CLIENTVERBOSE == "True":
				print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
				print("{}Type: Regular{}".format(bcolors.OKBLUE,bcolors.ENDC))
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.OKBLUE+"Type: Regular"+bcolors.ENDC+"\n").encode())
			
			
			for tag,type_list in State.profileData.items():
				if "tag" in filters_valid and filters_valid["tag"] != t:
					continue
				if Config.CLIENTVERBOSE == "True":
					print("{}Tag: {}{}".format(bcolors.OKBLUE,t,bcolors.ENDC))
				if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
					s.sendall((bcolors.OKBLUE+"Tag: "+t+bcolors.ENDC+"\n").encode())
				
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
							
							if Config.CLIENTVERBOSE == "True":
								print("{}Name: {}{}".format(bcolors.OKBLUE,mod,bcolors.ENDC))
							if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
								s.sendall((bcolors.OKBLUE+"Name: "+mod+bcolors.ENDC+"\n").encode())
							
							module_path = getKey(switcher_module,mod)
							if module_path != None:
								module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),mod)
								module_class.printData(data,s)
		
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()

def modules(cmd=None,state=None):
	filters = ["name","ip","type"]
	if len(cmd) == 2 and cmd[1] == "help":
		print("Filters: {}".format(filters))
		print("{}Usage: modules <e.g:name=Module_Ping ip=127.0.0.1||help||clear>{}".format(bcolors.OKBLUE,bcolors.ENDC))
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
	if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
	try:
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
			print("{}Modules Data{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
			s.sendall((bcolors.WARNING+"Modules Data"+bcolors.ENDC+"\n").encode())
	
		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "portscan"):
			if Config.CLIENTVERBOSE == "True":
				print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
				print("{}Type: Portscan{}".format(bcolors.OKBLUE,bcolors.ENDC))
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.OKBLUE+"Type: Portscan"+bcolors.ENDC+"\n").encode())
			
			for m,d in State.moduleData["portscan"].items():
				if "name" in filters_valid and filters_valid["name"] != m:
					continue
				
				if Config.CLIENTVERBOSE == "True":
					print("{}Name: {}{}".format(bcolors.OKBLUE,m,bcolors.ENDC))
				if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
					s.sendall((bcolors.OKBLUE+"Name: "+m+bcolors.ENDC+"\n").encode())
				
				for ip,v in d.items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					module_path = getKey(switcher_module,m)
					if module_path != None:
						module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),m)
						module_class.printData(v,s)
		
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())
				
		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "regular"):
			if Config.CLIENTVERBOSE == "True":
				print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
				print("{}Type: Regular{}".format(bcolors.OKBLUE,bcolors.ENDC))
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.OKBLUE+"Type: Regular"+bcolors.ENDC+"\n").encode())
			
			for m,d in State.moduleData["regular"].items():
				if "name" in filters_valid and filters_valid["name"] != m:
					continue
				
				if Config.CLIENTVERBOSE == "True":
					print("{}Name: {}{}".format(bcolors.OKBLUE,m,bcolors.ENDC))
				if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
					s.sendall((bcolors.OKBLUE+"Name: "+m+bcolors.ENDC+"\n").encode())
				
				for ip,v in d.items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					module_path = getKey(switcher_module,m)
					if module_path != None:
						module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),m)
						module_class.printData(v,s)
		
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()


def services(cmd=None,state=None):
	filters = ["type","module","profile","ip","port"]
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
	if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
	try:
		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "modules"):
			if Config.CLIENTVERBOSE == "True":
				print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
				print("{}Modules Data{}".format(bcolors.WARNING,bcolors.ENDC))
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.WARNING+"Modules Data"+bcolors.ENDC+"\n").encode())
		
			for m,d in State.moduleData["portscan"].items():
				if "name" in filters_valid and filters_valid["name"] != m:
					continue
				
				if Config.CLIENTVERBOSE == "True":
					print("{}Name: {}{}".format(bcolors.OKBLUE,m,bcolors.ENDC))
				if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
					s.sendall((bcolors.OKBLUE+"Name: "+m+bcolors.ENDC+"\n").encode())
				
				for ip,v in d.items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					module_path = getKey(switcher_module,m)
					if module_path != None:
						module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),m)
						module_class.printData(v,s)
		
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.OKBLUE,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.OKBLUE+"------------------------------------"+bcolors.ENDC+"\n").encode())

		if "type" not in filters_valid or ("type" in filters_valid and filters_valid["type"] == "profiles"):
			if Config.CLIENTVERBOSE == "True":
				print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
				print("{}Profiles Data{}".format(bcolors.WARNING,bcolors.ENDC))
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
				s.sendall((bcolors.WARNING+"Profiles Data"+bcolors.ENDC+"\n").encode())
			
			for tag,type_list in State.profileData.items():
				if "tag" in filters_valid and filters_valid["tag"] != t:
					continue
				if Config.CLIENTVERBOSE == "True":
					print("{}Tag: {}{}".format(bcolors.OKBLUE,tag,bcolors.ENDC))
				if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
					s.sendall((bcolors.OKBLUE+"Tag: "+tag+bcolors.ENDC+"\n").encode())
				
				for ip,port_list in type_list["portscan"].items():
					if "ip" in filters_valid and filters_valid["ip"] != ip:
						continue
					#print("{}---->Host: {}{}".format(bcolors.OKBLUE,ip,bcolors.ENDC))
					for port,mod_list in port_list.items():
						if "port" in filters_valid and filters_valid["port"] != port:
							continue
						for mod,data in mod_list.items():
							if "name" in filters_valid and filters_valid["name"] != mod:
								continue
				
							if Config.CLIENTVERBOSE == "True":
								print("{}Name: {}{}".format(bcolors.OKBLUE,mod,bcolors.ENDC))
							if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
								s.sendall((bcolors.OKBLUE+"Name: "+mod+bcolors.ENDC+"\n").encode())
				
							module_path = getKey(switcher_module,mod)
							if module_path != None:
								module_class = getattr(importlib.import_module(("src/"+module_path).replace("/",".")),mod)
								module_class.printData(data,s)
		
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()

def hosts(cmd=None,state=None):
	filters = ["module","profile","port"]
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

	for m,d in State.moduleData["portscan"].items():
		for ip in d:
	   		if ip not in hosts_array:
   				hosts_array.append(ip)
	for m,d in State.moduleData["regular"].items():
		for ip in d:
			if ip not in hosts_array:
				hosts_array.append(ip)
	for p,d in State.profileData.items():
		for ip in d["portscan"]:
			if ip not in hosts_array:
				hosts_array.append(ip)
		for ip in d["regular"]:
			if ip not in hosts_array:
				hosts_array.append(ip)

	s = None
	if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.LOGGERIP,int(Config.LOGGERPORT)))
	try:
		if Config.CLIENTVERBOSE == "True":
			print("{}------------------------------------{}".format(bcolors.WARNING,bcolors.ENDC))
			print("{}Hosts Data{}".format(bcolors.WARNING,bcolors.ENDC))
		if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
			s.sendall((bcolors.WARNING+"------------------------------------"+bcolors.ENDC+"\n").encode())
			s.sendall((bcolors.WARNING+"Hosts Data"+bcolors.ENDC+"\n").encode())
		
		for host in hosts_array:
			if Config.CLIENTVERBOSE == "True":
				print("{}[*]{} {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,host,bcolors.ENDC))
			if Config.LOGGERSTATUS == "True" and Config.LOGGERVERBOSE == "True":
				s.sendall((bcolors.OKBLUE+"[*]"+bcolors.ENDC+" "+bcolors.BOLD+host+bcolors.ENDC+"\n").encode())
	finally:
		if s != None:
			s.close()

def get_options(d,options,id=False):
	global state

	for k,v in d.items():
		if id == True:
			options.append(k)
		elif k == state.menu_state:
			options = get_options(v,options,True)
		elif isinstance(v, dict):
			options = get_options(v,options)
	return options

def help(cmd=None,state=None):
	if len(cmd) == 1:
		print("{}Global Command List:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in state.global_option:
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
	elif len(cmd) == 2:
		print("{}ToDo{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: help <empty||cmd>{}".format(bcolors.WARNING,bcolors.ENDC))

def ls(cmd=None,state=None):
	if len(cmd) == 1:
		print("{}Menu Command List:{}".format(bcolors.WARNING,bcolors.ENDC))
		options = []
		if state.module_state == "":
			options = get_options(state.menu_option,[])
		else:
			options = state.module_option
		for option in options:
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
	else:
		print("{}Usage: ls{}".format(bcolors.WARNING,bcolors.ENDC))


def switch(cmd=None,state=None):
	global completer
	
	state.menu_state = cmd[0]
	completer.update(get_options(state.menu_option,[])+state.global_option)

def exit(cmd=None,state=None):
	if len(cmd) == 1:
		state.menu_state = "exit"
	else:
		print("{}Usage: exit{}".format(bcolors.WARNING,bcolors.ENDC))


def invalid(cmds=None,state=None):
	print("{}Invalid Command! Use help/ls for options.{}".format(bcolors.WARNING,bcolors.ENDC))

def get_parent(d,t):
	out = t
	for k,v in d.items():
		if k == state.menu_state:
			return ("",True)
		elif isinstance(v, dict) and len(v) > 0 and out[1] != True:
			tmp = get_parent(v,t)
			if tmp[0] == "" and tmp[1]:
				out = (k,True)
			else:
				out = tmp
	return out

def back(cmd=None,state=None):
	global completer

	if len(cmd) == 1:
		if state.module_state == "":
			state.menu_state = get_parent(state.menu_option,("",False))[0]
			completer.update(get_options(state.menu_option,[])+state.global_option)
		else:
			state.env_option = {}
			state.module_class = ""
			state.module_state = ""
			completer.update(get_options(state.menu_option,[])+state.global_option)
	else:
		print("{}Usage: back{}".format(bcolors.WARNING,bcolors.ENDC))


def parse(cmd):
	if cmd == "":
		if state.module_state != "":
			return state.module_state
		else:
			return state.menu_state
	if not (cmd is None):
		values = cmd.split()

		if state.module_state == "":
			switcher_menu[state.menu_state].get(values[0], invalid)(values,state)
		else:
			switcher_menu["module"].get(values[0], invalid)(values,state)

		if state.module_state == "":
			return state.menu_state
		else:
			completer.update([x for x in state.module_option.keys()]+state.global_option)
			return state.module_state
	else:
		return "exit"

# OPTION VALUES
state = State()
switcher_menu = {"main":{"exit":exit,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles,"bof":switch,"external":switch,"internal":switch,"buckets":switch},"bof":{"badchars":bof_badchars,"pattern":bof_pattern,"offset":bof_offset,"lendian":bof_lendian,"nasm":bof_nasm,"nops":bof_nops,"notes":bof_notes,"exit":exit,"help":help,"ls":ls,"back":back,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles},"external":{"shellZ":switch,"use":external_use,"search":external_search,"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles},"internal":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles,"share":switch,"linux":switch,"windows":switch},"module":{"go":module_run,"get":module_get,"set":module_set,"exit":exit,"help":help,"ls":ls,"back":back,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles},"windows":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles},"linux":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles},"share":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles,"smb":internal_share,"ftp":internal_share,"http":internal_share,"powershell":internal_share,"vbscript":internal_share},"shellZ":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"services":services,"modules":modules,"profiles":profiles,"hosts":hosts,"linux_x86":external_shellz,"windows_x86":external_shellz,"php":external_shellz,"asp":external_shellz,"jsp":external_shellz,"notes":external_shellz},"buckets":{"exit":exit,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"modules":modules,"profiles":profiles,"open":buckets_open,"list":buckets_list,"add":buckets_add,"del":buckets_del}}

# AUTOCOMPLETE SETUP
completer = Completer(get_options(state.menu_option,[])+state.global_option)
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

# PROCESS MONITOR
watchdog = Monitor(state.procs)
watchdog.start()
