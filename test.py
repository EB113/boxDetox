import os, signal
import time

from .src.miscellaneous.config import Config,bcolors
from .src.menus.commons import State
from .src.imports.oscpPWN.httpserver import httpserver



def share_http(cmd=None,state=None):
	
	if len(cmd) == 2:
		if cmd[1] == "start":
			pid = os.fork()
			if pid:
				State.share_state["http"]["status"] = True
				State.share_state["http"]["pid"] = pid
				print("{}HTTP Server Started!{}".format(bcolors.OKGREEN,bcolors.ENDC))
			else:
				try:
					os.chdir(Config.PATH+"/db/shares")
					httpserver(4444)
					return
				except Exception as e:
					print("{}".format(e))
					print("{}".format(traceback.print_exc()))
					print("{}Address already in use!{}".format(bcolors.WARNING,bcolors.ENDC))

		elif cmd[1] == "stop":
			if State.share_state["http"]["status"]:
				os.kill(State.share_state["http"]["pid"], signal.SIGINT)
				State.share_state["http"]["status"] = False
				State.share_state["http"]["pid"] = 0
				print("{}HTTP Server Stopped!{}".format(bcolors.OKGREEN,bcolors.ENDC))
			else:
				print("{}HTTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
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


share_http(["http","start"])
share_http(["http","stop"])
