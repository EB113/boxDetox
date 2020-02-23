import queue

from ..miscellaneous.config import Config,bcolors

from ..modules.basic.ping	import Module_Ping

def module_run(cmd=None):
	if module_class.validate(env_option):
		if not procs.full():
			procs.put((module_state,module_class(env_option)))
		else:
			print("{}Too many tasks! ToDo dynamic task value manipulation.{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Wrong options! ToDo show option example forced class from Super.{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_get(cmd=None):
	if len(cmd) == 1:
		print("{}Module options:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in module_class.opt.keys():
			val = env_option.get(option)
			if val is None:
				print("{}[*] {}{}{} --> None".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
			else:
				print("{}[*] {}{}{} --> {}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option,val))
	else:
		print("{}Usage: get{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_set(cmd=None):
	if len(cmd) == 3:
		for option in module_class.opt.keys():
			if cmd[1] == option:
				env_option[cmd[1]] = cmd[2]
	else:
		print("{}Usage: set <option> <value>{}".format(bcolors.WARNING,bcolors.ENDC))
	return

# MODULE ENVIRONMENTAL VALUES
env_option = {}
module_option = {
					"get":{},
					"set":{},
					"go":{}
				}
switcher_module = {"modules/basic/ping":Module_Ping}
module_state = ""
module_class = ""
procs = queue.Queue(maxsize=Config.MAXTHREADS)
