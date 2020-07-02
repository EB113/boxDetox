import queue

from src.miscellaneous.config import Config

class State:
	menu_state = "main"
	bucket_state = ""
	module_state = ""
	module_class = ""
	actual_option = []
	global_option = ["profile","module","service","hosts","config","load","save","help","ls","back","exit"]
	config_option = ["SESSID","EDITOR","PATH","MAXMODULES","MAXPROFILES","MAXPROFILES","HTTPPORT","FTPPORT","FTPUSER","FTPPASS","SMBPORT","SMBUSER","SMBPASS","SHELLPORT","LOGGERIP","LOGGERPORT","LOGGERSTATUS","LOGGERVERBOSE","CLIENTVERBOSE"]
	menu_option = {
		"main": {
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
				"edit":{},
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
			"shares":{
				"smb":{},
				"ftp":{},
				"http":{},
				"powershell":{},
				"vbscript":{}
			}
		}
	}
	env_option = {}
	module_option = {
				"get":{},
				"set":{},
				"go":{}
			}
	procs = queue.Queue(maxsize=Config.CONFIG['CONCURRENCY']['MAXMODULES'])
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
