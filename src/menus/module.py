import queue

from src.menus.commons import State
from src.miscellaneous.config import Config,bcolors
from src.modules.basic.ping import Module_Ping

def module_run(cmd=None):
	if State.module_class.validate(State.env_option):
		if not State.procs.full():
			State.procs.put((State.module_state,State.module_class(State.env_option,"module",State.module_class.getName())))
		else:
			print("{}Too many module tasks!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Wrong options! ToDo show option example forced class from Super.{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_get(cmd=None):
	if len(cmd) == 1:
		print("{}Module options:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in State.module_class.opt.keys():
			val = State.env_option.get(option)
			if val is None:
				print("{}[*] {}{}{} --> None".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
			else:
				print("{}[*] {}{}{} --> {}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option,val))
	else:
		print("{}Usage: get{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_set(cmd=None):
	if len(cmd) == 3:
		for option in State.module_class.opt.keys():
			if cmd[1] == option:
				State.env_option[cmd[1]] = cmd[2]
	else:
		print("{}Usage: set <option> <value>{}".format(bcolors.WARNING,bcolors.ENDC))
	return

switcher_module = {"modules/basic/ping":"Module_Ping","modules/basic/ping1":"Module_Ping1","modules/basic/ping2":"Module_Ping2","modules/basic/ping3":"Module_Ping3","modules/basic/ping4":"Module_Ping4","modules/basic/ping5":"Module_Ping5","modules/basic/ping6":"Module_Ping6","modules/basic/ping7":"Module_Ping7","modules/basic/ping8":"Module_Ping8","modules/basic/ping9":"Module_Ping9","modules/portscan/basic":"Module_TCPCommon"}
