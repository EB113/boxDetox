import readline

from ..miscellaneous.completer import Completer
from ..miscellaneous.config import bcolors, Config

from ..profiles.profiler	import Profiler
from ..modules.monitor		import Monitor

from .commons import State
from .bof import bof_badchars,bof_pattern,bof_offset,bof_lendian,bof_nasm,bof_nops,bof_notes
from .module import module_run,module_get,module_set
from .external import external_use,external_search,external_shellz
from .internal import *
from .buckets import *

def config(cmd=None,state=None):

    if len(cmd) == 2 and cmd[1] == "list":
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

def services(cmd=None,state=None):
    print("{}Services:{}".format(bcolors.WARNING,bcolors.ENDC))
    #for host in hosts
    #print("{}Usage: help <empty||cmd>{}".format(bcolors.OKBLUE,bcolors.ENDC))

def hosts(cmd=None,state=None):
    print("{}Hosts:{}".format(bcolors.WARNING,bcolors.ENDC))
    #for host in hosts
    #print("{}Usage: help <empty||cmd>{}".format(bcolors.OKBLUE,bcolors.ENDC))


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
switcher_menu = {"main":{"exit":exit,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"bof":switch,"external":switch,"internal":switch,"buckets":switch},"bof":{"badchars":bof_badchars,"pattern":bof_pattern,"offset":bof_offset,"lendian":bof_lendian,"nasm":bof_nasm,"nops":bof_nops,"notes":bof_notes,"help":help,"ls":ls,"back":back,"config":config,"hosts":hosts,"services":services},"external":{"shellZ":switch,"use":external_use,"search":external_search,"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services},"internal":{"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"share":switch,"linux":switch,"windows":switch},"module":{"go":module_run,"get":module_get,"set":module_set,"help":help,"ls":ls,"back":back,"config":config,"hosts":hosts,"services":services},"windows":{"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services},"linux":{"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services},"share":{"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"smb":internal_share,"ftp":internal_share,"http":internal_share,"powershell":internal_share,"vbscript":internal_share},"shellZ":{"back":back,"help":help,"ls":ls,"config":config,"services":services,"hosts":hosts,"linux_x86":external_shellz,"windows_x86":external_shellz,"php":external_shellz,"asp":external_shellz,"jsp":external_shellz,"notes":external_shellz},"buckets":{"back":back,"help":help,"ls":ls,"config":config,"hosts":hosts,"services":services,"open":buckets_open,"list":buckets_list,"add":buckets_add,"del":buckets_del}}

# AUTOCOMPLETE SETUP
completer = Completer(get_options(state.menu_option,[]))
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

# PROCESS MONITOR
watchdog = Monitor(state.procs)
watchdog.start()

