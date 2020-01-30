import sys,os,re
import readline
import pyfiglet
import queue
import struct

from .miscellaneous.completer import *
from .miscellaneous.config import Config,bcolors

from .modules.monitor import Monitor
from .modules.basic.ping import Module_Ping

############### COMMAND LINE FUNCTIONS ##############
def run(cmd=None):
    if module_class.validate(env_option):
        if not procs.full():
            procs.put((module_state,module_class(env_option)))
        else:
            print("{}Too many tasks! ToDo dynamic task value manipulation.{}".format(bcolors.WARNING,bcolors.ENDC))
    else:
        print("{}Wrong options! ToDo show option example forced class from Super.{}".format(bcolors.WARNING,bcolors.ENDC))
    return

def get_opt(cmd=None):
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

def set_opt(cmd=None):
    if len(cmd) == 3:
        for option in module_class.opt.keys():
            if cmd[1] == option:
                env_option[cmd[1]] = cmd[2]
    else:
        print("{}Usage: set <option> <value>{}".format(bcolors.WARNING,bcolors.ENDC))
    return

def use(cmd=None):
    global module_class
    global module_state
    global completer
    if len(cmd) == 1:
        for r, d, f in os.walk(Config.PATH + "/src/modules"):
            for file in f:
                if bool(re.match(r"^[a-zA-Z0-9]+\.py$",file)) and (file[:-3] not in ["monitor","module"]):
                    print("{}[*] {}{}{}/{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,(r.split("modules"))[1][1:],file[:-3]))
        print("{}Usage: use <module||empty>{}".format(bcolors.WARNING,bcolors.ENDC))
    elif len(cmd)==2:
        if os.path.isfile(Config.PATH + "/src/modules/" + cmd[1] + ".py"):
            module_state = cmd[1]
            module_class = switcher_module.get(module_state,None)
            completer.update([x for x in module_option.keys()]+global_option)
        else:
            print("{}Module not found!{}".format(bcolors.WARNING,bcolors.ENDC))
    else:
        print("{}Usage: use <module||empty>{}".format(bcolors.WARNING,bcolors.ENDC))

def notes(cmd=None):
    if len(cmd) == 1:
        for item in switcher_cmd.get(menu_state, ["Empty List!"]):
            print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,item))
    else:
        print("{}Usage: cmds".format(bcolors.WARNING,bcolors.ENDC))

def bof_unique(cmd=None):
    out = ""
    if cmd != None and len(cmd) == 1:
        for i in range(0,256):
            out = out + "\\x" + format((ord(chr(i))), "x").zfill(2)
    elif len(cmd) == 2:
        out = ""
        badchars = cmd[1].split(r"\x")
        for i in range(0,256):
            tmp = format((ord(chr(i))), "x").zfill(2)
            if tmp not in badchars :
                out = out + "\\x" + tmp
    else:
        print("{}Usage: unique <empty||bad_char(\x0a)bad_char(\x0d)...>{}".format(bcolors.WARNING,bcolors.ENDC))
        return
    print("\nbadchars =")
    print("\"", end = "")
    numChars = len(out)
    for i in range(0,numChars):
        if i % 64 == 0 and i != 0:
            print("\"")
            print("\"", end = "")
        print(out[i], end = "")
    #print("{}".format(out), end = "")
    print("\";\n")
    print("Number of characters: " + str(round(numChars/4)) + "\n")
    
def bof_pattern(cmd=None):
    if len(cmd) == 2:
        # CHECK IF NUMBER
        os.system("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l " + cmd[1])
    else:
        print("{}Usage: pattern <size>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_offset(cmd=None):
    if len(cmd) == 2:
        # CHECK IF NUMBER
        os.system("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q " + cmd[1])
    else:
        print("{}Usage: offset <pattern>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_lendian(cmd=None):
    if len(cmd) == 2:
        # CHECK IF ADDRESS
        if bool(re.match("^[0-9a-zA-Z]+$",cmd[1])):
            print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,struct.pack("<I",int("0x"+cmd[1],16))))
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
        for option in global_option.keys():
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
                        "enum":{
                            "use":{},
                            },
                        "bof" : {
                            "badchars":{},
                            "pattern":{},
                            "offset":{},
                            "lendian":{},
                            "nasm":{},
                            "notes":{},
                            },
                        "exit":{}
                        }
                  }
switcher_menu = {"main":{"exit":exit,"help":help,"ls":ls,"bof":state,"enum":state},"bof":{"badchars":bof_unique,"pattern":bof_pattern,"offset":bof_offset,"lendian":bof_lendian,"nasm":bof_nasm,"notes":notes,"help":help,"ls":ls,"back":back},"enum":{"use":use,"back":back,"help":help,"ls":ls},"module":{"go":run,"get":get_opt,"set":set_opt,"help":help,"ls":ls,"back":back}}
menu_state   = "main"
module_option = {
                    "get":{},
                    "set":{},
                    "go":{}
                }
switcher_module = {"basic/ping":Module_Ping}
module_state = ""
module_class = ""
# MODULE ENVIRONMENTAL VALUES
env_option = {}

# NOTES
switcher_cmd = {
                "bof" : [r'!mona bytearray -cpb "\x00"',r'!mona compare -f bytearray.txt -a esp',r'!mona jmp -r esp -cpb "\x00"']
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
