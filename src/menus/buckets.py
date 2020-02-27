import os

from ..miscellaneous.config import bcolors, Config

def buckets_open(cmd=None,state=None):
	if len(cmd) == 2:
		for subdirs,dirs,files in os.walk(Config.PATH+"/db/buckets"):
			print(subdirs)
			print(dirs)
			print(files)
		return
	else:
		print("{}Usage: back{}".format(bcolors.WARNING,bcolors.ENDC))

def buckets_list(cmd=None,state=None):
	first = True
	if len(cmd) == 1:
		for subdirs,dirs,files in os.walk(Config.PATH+"/db/buckets"):
			if first:
				first = False
				continue
			print("{}[*] {}{}".format(bcolors.OKBLUE,subdirs.split("/")[-1],bcolors.ENDC))
		return
	else:
		print("{}Usage: back{}".format(bcolors.WARNING,bcolors.ENDC))
	
def buckets_add(cmd=None,state=None):
	if not os.path.isdir(Config.PATH+"/db/buckets/"+cmd[1]):
		try:
			os.mkdir(Config.PATH+"/db/buckets/"+cmd[1])
		except:
			print("{}Check {} permissions!{}".format(bcolors.WARNING,Config.PATH+"/db/buckets",bcolors.ENDC))
			
def buckets_del(cmd=None,state=None):
	if os.path.isdir(Config.PATH+"/db/buckets/"+cmd[1]):
		try:
			for subdirs,dirs,files in os.walk(Config.PATH+"/db/buckets"+cmd[1]):
				return
		except:
			print("{}Check {} permissions!{}".format(bcolors.WARNING,Config.PATH+"/db/buckets",bcolors.ENDC))
