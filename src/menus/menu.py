import pyfiglet,readline

from ..miscellaneous.completer import Completer
from ..miscellaneous.config import bcolors

from ..profiles.profiler	import Profiler
from ..modules.monitor		import Monitor

from .bof import bof_badchars,bof_pattern,bof_offset,bof_lendian,bof_nasm,bof_nops,bof_notes
from .module import module_run,module_get,module_set,module_state,procs
from .external import external_use,external_search
from .internal import *

def get_options(d,options,id=False):
	for k,v in d.items():
		if id == True:
			options.append(k)
		elif k == menu_state:
			options = get_options(v,options,True)
		elif isinstance(v, dict):
			options = get_options(v,options)
	return options

def help(cmd=None):
	if len(cmd) == 1:
		print("{}Global Command List:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in global_option:
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
	elif len(cmd) == 2:
		print("{}ToDo{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: help <empty||cmd>{}".format(bcolors.WARNING,bcolors.ENDC))

def ls(cmd=None):
	if len(cmd) == 1:
		print("{}Menu Command List:{}".format(bcolors.WARNING,bcolors.ENDC))
		options = []
		if module_state == "":
			options = get_options(menu_option,[],menu_state)
		else:
			options = module_option
		for option in options:
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
	else:
		print("{}Usage: ls{}".format(bcolors.WARNING,bcolors.ENDC))


def state(cmd=None):
	global menu_state
	global completer
	
	menu_state = cmd[0]
	completer.update(get_options(menu_option,[],menu_state)+global_option)

def exit(cmd=None):
	global menu_state
	if len(cmd) == 1:
		menu_state = "exit"
	else:
		print("{}Usage: exit{}".format(bcolors.WARNING,bcolors.ENDC))


def invalid(cmds=None):
	print("{}Invalid Command! Use help/ls for options.{}".format(bcolors.WARNING,bcolors.ENDC))

def get_parent(d,t):
	out = t
	for k,v in d.items():
		if k == menu_state:
			return ("",True)
		elif isinstance(v, dict) and len(v) > 0:
			tmp = get_parent(v,t)
			if tmp[0] == "" and tmp[1] == True:
				return (k,True)
			else:
				out = tmp
		else:
			return t
	return out

def back(cmd=None):
	global env_option
	global menu_state
	global module_state
	global completer

	if len(cmd) == 1:
		if module_state == "":
			menu_state = get_parent(menu_option,("",False))[0]
			completer.update(get_options(menu_option,[],menu_state)+global_option)
		else:
			env_option = {}
			module_class = ""
			module_state = ""
			completer.update(get_options(menu_option,[],menu_state)+global_option)
	else:
		print("{}Usage: back{}".format(bcolors.WARNING,bcolors.ENDC))


def parse(cmd):
	if cmd == "":
		if module_state != "":
			return module_state
		else:
			return menu_state
	if not (cmd is None):
		values = cmd.split()

		if module_state == "":
			switcher_menu[menu_state].get(values[0], invalid)(values)
		else:
			switcher_menu["module"].get(values[0], invalid)(values)

		if module_state == "":
			return menu_state
		else:
			completer.update([x for x in module_option.keys()]+global_option)
			return module_state
	else:
		return "exit"

# OPTION VALUES
global_option = ["help","ls","back"]
menu_option = {
	"main": {
		"internal":{
			"file_transfer":{},
			"linux":{},
			"windows":{}
			},
		"external":{
			"use":{},
			"search":{}
			},
		"bof" : {
			"badchars":{},
			"pattern":{},
			"offset":{},
			"lendian":{},
			"nasm":{},
			"nops":{},
			"notes":{}
			},
		"exit":{}
	}
}
switcher_menu = {"main":{"exit":exit,"help":help,"ls":ls,"bof":state,"external":state,"internal":state},"bof":{"badchars":bof_badchars,"pattern":bof_pattern,"offset":bof_offset,"lendian":bof_lendian,"nasm":bof_nasm,"nops":bof_nops,"notes":bof_notes,"help":help,"ls":ls,"back":back},"external":{"use":external_use,"search":external_search,"back":back,"help":help,"ls":ls},"internal":{"back":back,"help":help,"ls":ls,"file_transfer":state,"linux":state,"windows":state},"module":{"go":module_run,"get":module_get,"set":module_set,"help":help,"ls":ls,"back":back},"windows":{"back":back,"help":help,"ls":ls},"linux":{"back":back,"help":help,"ls":ls},"file_transfer":{"back":back,"help":help,"ls":ls}}
menu_state = "main"

# AUTOCOMPLETE SETUP
completer = Completer(get_options(menu_option,[],menu_state))
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

# PROCESS MONITOR
watchdog = Monitor(procs)
watchdog.start()

# BANNER
print("{}{}{}".format(bcolors.HEADER,pyfiglet.figlet_format("oscpPWN"),bcolors.ENDC))
