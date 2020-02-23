import sys,os,re
import readline
import pyfiglet
import queue
import clipboard

from .miscellaneous.completer import *
from .miscellaneous.config import Config,bcolors

from .profiles.profiler		import Profiler
from .modules.monitor		import Monitor
from .modules.basic.ping	import Module_Ping

############### COMMAND LINE FUNCTIONS ##############
def module_run(cmd=None):
	if module_class.validate(env_option):
		if not procs.full():
			procs.put((module_state,module_class(env_option)))
		else:
			print("{}Too many tasks! ToDo dynamic task value manipulation.{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Wrong options! ToDo show option example forced class from Super.{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_get_opt(cmd=None):
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

def module_set_opt(cmd=None):
	if len(cmd) == 3:
		for option in module_class.opt.keys():
			if cmd[1] == option:
				env_option[cmd[1]] = cmd[2]
	else:
		print("{}Usage: set <option> <value>{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def enum_use(cmd=None):
	if len(cmd)==2:
		if bool(re.match(r"^modules\/.+",cmd[1])):
			global module_class
			global module_state
			global completer
			
			if os.path.isfile(Config.PATH + "/src/" + cmd[1] + ".py"):
				module_state = cmd[1]
				module_class = switcher_module.get(module_state,None)
				completer.update([x for x in module_option.keys()]+global_option)
			else:
				print("{}Module not found!{}".format(bcolors.WARNING,bcolors.ENDC))
		elif bool(re.match(r"^profiles\/.+",cmd[1])):
			if os.path.isfile(Config.PATH + "/src/" + cmd[1] + ".tpl"):
				try:
					tpl = json.load(open(Config.PATH+"/src/"+cmd[1]+".tpl"))
				except Exception as e:
					print("{}File does not contain valid JSON!{}".format(bcolors.WARNING,bcolors.ENDC))
				else:
					try:
						if Profiler.validate(tpl):
							Profiler(tpl).start()
						else:
							print("{}File .tpl not in expected format!{}".format(bcolors.WARNING,bcolors.ENDC))
					except Exception as e:
						print("{}".format(e))
						print("{}".format(traceback.print_exc()))
			else:
				print("{}Profile not found!{}".format(bcolors.WARNING,bcolors.ENDC))
		else:
			print("{}Invalid Module/Profile!{}".format(bcolors.WARNING,bcolors.ENDC))


	else:
		print("{}Usage: use <Module||Profile>{}".format(bcolors.WARNING,bcolors.ENDC))


def enum_search_aux(opt):

	if opt == "modules":
		ext = "\.py"
		ext_cut = -3
	else:
		ext = "\.tpl"
		ext_cut = -4

	for r, d, f in os.walk(Config.PATH + "/src/"+opt):
		for file in f:
			if bool(re.match(r"^[a-zA-Z0-9]+"+ext+"$",file)) and (file[:-3] not in ["monitor","module","profiler","portscanner"]):
				if r.split(opt)[1][1:] != "":
					print("{}[*] {}{}{}/{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,opt,(r.split(opt))[1][1:],file[:ext_cut]))
				else:
					print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,opt,file[:ext_cut]))

def enum_search(cmd=None):
	if len(cmd) == 1:
		enum_search_aux("modules")
		enum_search_aux("profiles")
	elif len(cmd) == 2 and (cmd[1] == "modules" or cmd[1] == "profiles"):
		enum_search_aux(cmd[1])
	else:
		print("{}Usage: list <module||profile||empty>{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def notes(cmd=None):
	if len(cmd) == 1:
		for item in switcher_cmd.get(menu_state, ["Empty List!"]):
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,item))
	else:
		print("{}Usage: cmds".format(bcolors.WARNING,bcolors.ENDC))

def bof_badchars(cmd=None):
	out = ""
	outFormat = "c"
	if cmd != None and len(cmd) == 1:
		for i in range(0,256):
			out = out + "\\x" + format((ord(chr(i))), "x").zfill(2)
	elif len(cmd) == 2 or len(cmd) == 3:
		if len(cmd) == 3:
			outFormat = cmd[2]
		elif len(cmd) == 2 and cmd[1][0] != "\\":
			outFormat = cmd[1]
		out = ""
		badchars = cmd[1].split(r"\x")
		for i in range(0,256):
			tmp = format((ord(chr(i))), "x").zfill(2)
			if tmp not in badchars :
				out = out + "\\x" + tmp
	else:
		print("{}Usage: badchars [\\x00\\x0a...] [c | python]{}".format(bcolors.WARNING,bcolors.ENDC))
		return
	badcharcp = ""
	numChars = len(out)
	for i in range(0,numChars):
		if i % 64 == 0 and i != 0:
			badcharcp += "\"\n"
			badcharcp += "\""
		badcharcp += out[i]
	if outFormat == "c":
		badcharcp = "badchars =\n\"" + badcharcp + "\";\n"
	elif outFormat == "python":
		badcharcp = "badchars = (\n\"" + badcharcp + "\")\n"
	else:
		print("{}Invalid output format specified, defaulting to c\n(Accepted formats are \"c\" and \"python\"){}".format(bcolors.WARNING,bcolors.ENDC))
		badcharcp = "badchars =\n\"" + badcharcp + "\";\n"
	print("\n" + badcharcp)
	clipboard.copy(badcharcp)
	print("Number of characters: " + str(round(numChars/4)) + "\n")
	print("{}* Badchars copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_pattern(cmd=None):
	if len(cmd) == 2:
		# CHECK IF NUMBER
		patterncm = ("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l " + cmd[1])
		print(patterncm + "\n")
		patterncp = os.popen(patterncm).read()
		print(patterncp)
		clipboard.copy(patterncp)
		print("{}* Offset copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: pattern <length>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_offset(cmd=None):
	if len(cmd) == 2:
		# CHECK IF NUMBER
		offsetcm =("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q " + cmd[1])
		print(offsetcm + "\n")
		offsetcp = os.popen(offsetcm).read()
		print(offsetcp)
		offsetpp = os.popen(offsetcm + "|awk -F' ' '{print $6}'").read()
		clipboard.copy(offsetpp)
		print("{}* Offset copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: offset <pattern>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_lendian(cmd=None):
	if len(cmd) == 2:
		# CHECK IF ADDRESS
		if bool(re.match("^[0-9a-zA-Z]+$",cmd[1])):
			n=len(cmd[1])-2
			if n == 6 or n == 14:
				out=""
				while(n > -2):
					out+="\\x" + cmd[1][n]+cmd[1][n+1]
					n-=2
				print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,out))
				clipboard.copy(out)
				print("{}* Lendian address copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
			else:
				print("{}Wrong address format! Use 64bit or 32bit address.{}".format(bcolors.WARNING,bcolors.ENDC))
		else:
			print("{}Invalid Address!e.g:080414C3{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: lendian <address>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_nasm(cmd=None):
	if len(cmd) == 1:
		# CHECK IF NUMBER
		os.system("/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb")
	else:
		print("{}Usage: nasm{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_nops(cmd=None):
	num = 1
	if len(cmd) == 1:
		print("{}How many nops do you want?{}".format(bcolors.WARNING,bcolors.ENDC))
		num = int(sys.stdin.readline())
		print("\nHere ya go:\n")
		out = "\\x90" * num
		print(out + "\n")
		clipboard.copy(out)
		print("{}* Nops copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	elif len(cmd) == 2:
		num = int(cmd[1])
		out = "\\x90" * num
		print("\n" + out + "\n")
		clipboard.copy(out)
		print("{}* Nops copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: nops number{}".format(bcolors.WARNING,bcolors.ENDC))


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
			options = get_options(menu_option,[])
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
	completer.update(get_options(menu_option,[])+global_option)

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
			completer.update(get_options(menu_option,[])+global_option)
		else:
			env_option = {}
			module_class = ""
			module_state = ""
			completer.update(get_options(menu_option,[])+global_option)
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
							"notes":{},
							},
						"exit":{}
						}
				  }
switcher_menu = {"main":{"exit":exit,"help":help,"ls":ls,"bof":state,"external":state,"internal":state},"bof":{"badchars":bof_badchars,"pattern":bof_pattern,"offset":bof_offset,"lendian":bof_lendian,"nasm":bof_nasm,"nops":bof_nops,"nops":bof_nops,"notes":notes,"help":help,"ls":ls,"back":back},"external":{"use":enum_use,"search":enum_search,"back":back,"help":help,"ls":ls},"internal":{"back":back,"help":help,"ls":ls,"file_transfer":state,"linux":state,"windows":state},"module":{"go":module_run,"get":module_get_opt,"set":module_set_opt,"help":help,"ls":ls,"back":back},"windows":{"back":back,"help":help,"ls":ls},"linux":{"back":back,"help":help,"ls":ls},"file_transfer":{"back":back,"help":help,"ls":ls}}
menu_state	 = "main"
module_option = {
					"get":{},
					"set":{},
					"go":{}
				}
switcher_module = {"modules/basic/ping":Module_Ping}
module_state = ""
module_class = ""
# MODULE ENVIRONMENTAL VALUES
env_option = {}

# NOTES
switcher_cmd = {
				"bof" : [r'!mona bytearray -b "\x00"',r'!mona compare -f bytearray.txt -a esp',r'!mona jmp -r esp -cpb "\x00"']
			}

# LOAD SETTINGS
config = Config()

# PROCESS MONITOR
procs = queue.Queue(maxsize=Config.MAXTHREADS)
watchdog = Monitor(procs)
watchdog.start()

# AUTOCOMPLETE SETUP
completer = Completer(get_options(menu_option,[]))
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

# BANNER
print("{}{}{}".format(bcolors.HEADER,pyfiglet.figlet_format("oscpPWN"),bcolors.ENDC))
