#from ..imports.impacket import smbserver

import os, signal
import time

from ..miscellaneous.config import Config,bcolors
from .commons import State

def share_smb(cmd=None,state=None):
    return
def share_ftp(cmd=None,state=None):
    return
def share_http(cmd=None,state=None):
    
    if len(cmd) == 2:
        if cmd[1] == "start":
            pid = os.fork()
            if pid:
                State.share_state["http"]["status"] = True
                State.share_state["http"]["pid"] = pid
            else:
                try:
                    os.system("python3.7 /mnt/hgfs/Base/tmp/oscpPWN/src/imports/oscpPWN/httpserver.py")
                except:
                    print("{}Address already in use!{}".format(bcolors.WARNING,bcolors.ENDC))

        elif cmd[1] == "stop":
            if State.share_state["http"]["status"]:
                os.kill(State.share_state["http"]["pid"], signal.SIGINT)
                State.share_state["http"]["status"] = False
                State.share_state["http"]["pid"] = 0

        elif cmd[1] == "status":
            if State.share_state["http"]["status"]:
                print("{}HTTP Server Active!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                print("{}HTTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
            
        elif cmd[1] == "cmd":
            print("{}wget http://{}/{{PATH}}{}".format(bcolors.OKBLUE,Config.HOSTIP,bcolors.ENDC))
            
        else:
            print("{}Usage: http <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
            return
    else:
        print("{}Usage: http <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
        return

def share_powershell(cmd=None,state=None):
    return
def share_vbscript(cmd=None,state=None):
    return

switcher_share = {"smb":share_smb,"ftp":share_ftp,"http":share_http,"powershell":share_powershell,"vbscript":share_vbscript}


def internal_share(cmd=None,state=None):

    switcher_share.get(cmd[0],"Invalid!")(cmd,state)
