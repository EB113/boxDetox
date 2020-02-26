#from ..imports.impacket import smbserver

import os, signal
import time

from ..miscellaneous.config import Config,bcolors
from .commons import State
from ..imports.oscpPWN.httpserver import httpserver
from ..imports.oscpPWN.ftpserver import ftpserver

def share_smb(cmd=None,state=None):
	return

def share_ftp(cmd=None,state=None):
	if len(cmd) == 2:
		if cmd[1] == "start":
			pid = os.fork()
			if pid:
				State.share_state["ftp"]["status"] = True
				State.share_state["ftp"]["pid"] = pid
				print("{}FTP Server Started!{}".format(bcolors.OKGREEN,bcolors.ENDC))
			else:
				try:
					os.chdir(Config.PATH+"/db/shares")
					ftpserver(21)
					return
				except Exception as e:
					print("{}".format(e))
					print("{}".format(traceback.print_exc()))
					print("{}Address already in use!{}".format(bcolors.WARNING,bcolors.ENDC))

		elif cmd[1] == "stop":
			if State.share_state["ftp"]["status"]:
				os.kill(State.share_state["ftp"]["pid"], signal.SIGINT)
				State.share_state["ftp"]["status"] = False
				State.share_state["ftp"]["pid"] = 0
				print("{}FTP Server Stopped!{}".format(bcolors.OKGREEN,bcolors.ENDC))
			else:
				print("{}FTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
		elif cmd[1] == "status":
			if State.share_state["ftp"]["status"]:
				print("{}FTP Server Active!{}".format(bcolors.OKGREEN,bcolors.ENDC))
			else:
				print("{}FTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
			
		elif cmd[1] == "cmd":
			print("{}wget http://{}/{{PATH}}{}".format(bcolors.OKBLUE,Config.HOSTIP,bcolors.ENDC))
			
		else:
			print("{}Usage: ftp <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
			return
	else:
		print("{}Usage: ftp <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
		return
	return

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

def share_powershell(cmd=None,state=None):
	return
def share_vbscript(cmd=None,state=None):
	return

switcher_share = {"smb":share_smb,"ftp":share_ftp,"http":share_http,"powershell":share_powershell,"vbscript":share_vbscript}


def internal_share(cmd=None,state=None):

	switcher_share.get(cmd[0],"Invalid!")(cmd,state)
