import queue

from src.menus.commons import State
from src.miscellaneous.config import Config,bcolors
from src.modules.basic.ping import Module_Ping

def module_run(cmd=None,state=None):
	if state.module_class.validate(state.env_option):
		if not state.procs.full():
			state.procs.put((state.module_state,state.module_class(state.env_option,"module")))
		else:
			print("{}Too many module tasks!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Wrong options! ToDo show option example forced class from Super.{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_get(cmd=None,state=None):
	if len(cmd) == 1:
		print("{}Module options:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in state.module_class.opt.keys():
			val = state.env_option.get(option)
			if val is None:
				print("{}[*] {}{}{} --> None".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
			else:
				print("{}[*] {}{}{} --> {}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option,val))
	else:
		print("{}Usage: get{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_set(cmd=None,state=None):
	if len(cmd) == 3:
		for option in state.module_class.opt.keys():
			if cmd[1] == option:
				state.env_option[cmd[1]] = cmd[2]
	else:
		print("{}Usage: set <option> <value>{}".format(bcolors.WARNING,bcolors.ENDC))
	return

switcher_module = {"modules/basic/ping":Module_Ping}
