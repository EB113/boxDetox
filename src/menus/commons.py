import queue

from src.miscellaneous.config import Config

class State:
	menu_state = "main"
	bucket_state = ""
	module_state = ""
	module_class = ""
	global_option = ["profiles","modules","services","hosts","config","load","save","help","ls","back","exit"]
	menu_option = {
		"main": {
			"internal":{
				"share":{
					"smb":{},
					"ftp":{},
					"http":{},
					"powershell":{},
					"vbscript":{}
					},
				"linux":{},
				"windows":{}
			},
			"external":{
				"shellZ":{
					"linux_x86":{},
					"windows_x86":{},
					"php":{},
					"asp":{},
					"jsp":{},
					"notes":{}
					},
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
				"notes":{}
			},
			"buckets":{
				"open":{},
				"list":{},
				"add":{},
				"del":{}
				}
		}
	}
	env_option = {}
	module_option = {
				"get":{},
				"set":{},
				"go":{}
			}
	procs = queue.Queue(maxsize=Config.MAXMODULES)
	share_state = {
			"smb":{
				"status":False,
				"pid":0
			},
			"ftp":{
				"status":False,
				"pid":0
			},
			"http":{
				"status":False,
				"pid":0
			}
		}
	moduleData = {"portscan":{},"regular":{}}
	profileData = {}

	def __init__(self):
		pass

