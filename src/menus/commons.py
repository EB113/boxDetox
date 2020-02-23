import queue

from ..miscellaneous.config import Config

class State:
	menu_state = "main"
	module_state = ""
	module_class = ""
	global_option = ["help","ls","back"]
	menu_option = {
		"main": {
			"internal":{
				"file_transfer":{},
				"linux":{},
				"windows":{}
			},
			"external":{
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
			"exit":{}
		}
	}
	env_option = {}
	module_option = {
				"get":{},
				"set":{},
				"go":{}
			}
	procs = queue.Queue(maxsize=Config.MAXTHREADS)

	def __init__(self):
		pass
