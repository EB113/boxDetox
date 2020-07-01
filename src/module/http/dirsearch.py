import threading,socket
import netaddr,os,subprocess,re

from src.miscellaneous.config import Config,bcolors
from src.module.module import Module

import json,time,traceback

def target(val=None):
	if val is None:
		return False
	else:
		return bool(re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}(\/[0-9]{0,2}){0,1}$",val))

def secure(val=None):
	if val is None:
		return False
	else:
		return (val == "True" or val == "False")

def wlist(val=None):
	if val is not None and type(val)==str and val in ["small","common","big"]:
		return True
	else:
		return False

def port(val=None):
    if val is None:
        return False
    else:
        try:
            int(val)
            return True
        except:
            return False

#Need to see how to deal with multiple flags
def flag(val=None):
	return True

def parseJSON(path=None):
	json_data= {}
	with open(path,"r") as json_file:
		try:
			json_data = json.load(json_file)
		except Exception as e:
			print("{}{}DirSearch: CONNECTION TIMEOUT{}".format(bcolors.BOLD,bcolors.FAIL,bcolors.ENDC))
			return None
			
	return json_data

class Module_HTTP_dirsearch(Module):

	opt_static = {"target":target,"secure":secure}#{"target":target,"output":flag}
	opt_dynamic = {"port":port,"wlist":wlist}#{"target":target,"output":flag}

	def __init__(self,opt_dict,mode,module_name,profile_tag=None,profile_port=None):
		threading.Thread.__init__(self)
		super().__init__(opt_dict,mode,module_name,profile_tag,profile_port)

	def run(self):
		lst = Module_HTTP_dirsearch.targets(self.opt_dict["target"])
		fn = Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID'] + "/tmp/dirsearch.json"
		data = {}
		for ip in lst:
			if not self.flag.is_set():
				#Fix tTHIS!!!!!!!! PORT PROFILE AND NOT MODULE IDIOT
				if "port" in self.opt_dict:
					port = self.opt_dict["port"]
				else:
					port = self.profile_port

				if self.opt_dict["secure"] == "False":
					if ("wlist" in self.opt_dict) and (self.opt_dict["wlist"] is not None):
						proc = os.popen("/bin/bash -c 'python3 "+ Config.CONFIG['GENERAL']['PATH'] +"/3rd/dirsearch/dirsearch.py -u http://"+ ip +":"+port+"/ -E -w /usr/share/wordlists/dirb/"+self.opt_dict["wlist"]+".txt --json-report="+ fn+"'")
					else:
						proc = os.popen("/bin/bash -c 'python3 "+ Config.CONFIG['GENERAL']['PATH'] +"/3rd/dirsearch/dirsearch.py -u http://"+ ip +":"+port+"/ -E -w /usr/share/wordlists/dirb/common.txt --json-report="+ fn+"'")
				else:
					if ("wlist" in self.opt_dict) and (self.opt_dict["wlist"] is not None):
						proc = os.popen("/bin/bash -c 'python3 "+ Config.CONFIG['GENERAL']['PATH'] +"/3rd/dirsearch/dirsearch.py -u https://"+ ip +":"+port+"/ -E -w /usr/share/wordlists/dirb/"+self.opt_dict["wlist"]+".txt --json-report="+ fn+"'")
					else:
						proc = os.popen("/bin/bash -c 'python3 "+ Config.CONFIG['GENERAL']['PATH'] +"/3rd/dirsearch/dirsearch.py -u https://"+ ip +":"+self.profile_port+"/ -E -w /usr/share/wordlists/dirb/common.txt --json-report="+ fn+"'")
				proc.read()
				proc.close()
				jsonOut = parseJSON(fn)
				if jsonOut is None:
					return
				out = json.dumps(parseJSON(fn), indent=4, sort_keys=True)
				if self.mode == "profile": 
					fd = open(Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID']+"/profile/"+self.profile_tag+"/"+ip+"/"+self.profile_port+"/dirsearch","w")
					fd.write(out)
					fd.close()
				data[ip] = out
				self.storeDataRegular(data)
				if Config.CONFIG['OUTPUT']['LOGGERVERBOSE'] == "True":
					with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
						s.connect((Config.CONFIG['LOGGER']['LOGGERIP'],int(Config.CONFIG['LOGGER']['LOGGERPORT'])))
						try:
							self.printData(out,s,True)
						finally:
							s.close()
				if Config.CONFIG['OUTPUT']['CLIENTVERBOSE'] == "True":
					self.printData(out,enclose=True)
			else:
				break
		return
