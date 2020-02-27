from . import commons
import sys,os,re,json

from ..miscellaneous.config import Config,bcolors
from .module import switcher_module

def external_shellz():
    return

def external_use(cmd=None,state=None):
	if len(cmd)==2:
		if bool(re.match(r"^modules\/.+",cmd[1])):
			
			if os.path.isfile(Config.PATH + "/src/" + cmd[1] + ".py"):
				state.module_state = cmd[1]
				state.module_class = switcher_module.get(state.module_state,None)
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


def external_search_aux(opt,state=None):

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

def external_search(cmd=None,state=None):
	if len(cmd) == 1:
		external_search_aux("modules")
		external_search_aux("profiles")
	elif len(cmd) == 2 and (cmd[1] == "modules" or cmd[1] == "profiles"):
		external_search_aux(cmd[1])
	else:
		print("{}Usage: list <module||profile||empty>{}".format(bcolors.WARNING,bcolors.ENDC))
	return