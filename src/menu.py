import sys,os
import readline
import pyfiglet

from .miscellaneous.completer import *
from .config import Config

############ OUTPUT GRAPHICS ################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

############### COMMAND LINE FUNCTIONS ##############
def notes(cmd=None):
    if cmd != None and len(cmd) == 1:
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
        print("{}Usage: unique <empty||bad_char(\x0a),bad_char(\x0d),...>{}".format(bcolors.WARNING,bcolors.ENDC))
        return
    print("{}".format(out))

def bof_pattern(cmd=None):
    if len(cmd) == 2:
        # CHECK IF NUMBER
        os.system("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l " + cmd[1])
    else:
        print("{}Usage: pattern <size>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_offset(cmd=None):
    if len(cmd) == 3:
        # CHECK IF NUMBER
        os.system("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l " + cmd[1] + " -q " + cmd[2])
    else:
        print("{}Usage: offset <size> <pattern>{}".format(bcolors.WARNING,bcolors.ENDC))

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
    print("Command list:")
    options = get_options(menu_option,[])
    for option in options:
        print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))

def state(cmd=None):
    global menu_state
    global completer
    menu_state = cmd[0]
    completer.update(get_options(menu_option,[]))

def exit(cmd=None):
    global menu_state
    menu_state = "exit"

def invalid(cmds=None):
    print("{}Invalid Command! Use help for options.{}".format(bcolors.WARNING,bcolors.ENDC))

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
    global menu_state
    menu_state = get_parent(menu_option,("",False))[0]

def parse(cmd):
    values = cmd.split()
    switcher_menu[menu_state].get(values[0], invalid)(values)
    #history(cmd)
    return menu_state

# MENU OPTIONS VALUES
menu_option = {
                    "main": {
                        "bof" : {
                            "unique":{},
                            "pattern":{},
                            "offset":{},
                            "nasm":{},
                            "notes":{},
                            "help":{},
                            "back":{}
                            },
                        "help":{},
                        "exit":{}
                        }
                  }
switcher_menu = {"main":{"exit":exit,"help":help,"bof":state},"bof":{"unique":bof_unique,"pattern":bof_pattern,"offset":bof_offset,"nasm":bof_nasm,"notes":notes,"help":help,"back":back}}
menu_state   = "main"

# LOAD SETTINGS
config = Config()

# AUXILIARY CMDS PER MODULE
switcher_cmd = {
                "bof" : ['!mona bytearray -b ""','!mona compare -f c:\logs\3CTftpSvc\bytearray.txt -a 00A5E9A8']
            }

# AUTOCOMPLETE SETUP
completer = Completer(get_options(menu_option,[]))
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

# BANNER
print("{}{}{}".format(bcolors.HEADER,pyfiglet.figlet_format("oscpPWN"),bcolors.ENDC))
