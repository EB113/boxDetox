import threading
import re

from src.menus.commons import State

class Module(threading.Thread):

	def __init__(self,opt_dict=None,mode=None,module_name=None,profile_tag=None,profile_port=None):
		self.flag = threading.Event()
		if opt_dict == None:
			raise ValueError("Module argument opt_dict is None!")
		self.opt_dict = opt_dict
		if mode == None:
			raise ValueError("Module argument mode is None!")
		self.mode = mode
		if module_name == None:
			raise ValueError("Module argument module_name is None!")
		self.module_name = module_name		
		#if profile_tag != None and profile_port == None:
			#raise ValueError("Profile argument profile_port is None!")
		self.profile_tag = profile_tag
		self.profile_port = profile_port
	
	@staticmethod
	def validate(opt_dict):
		raise NotImplementedError
	
	@staticmethod
	def getName():
		raise NotImplementedError
	
	@staticmethod
	def printData(data,conn=None):
		raise NotImplementedError

	def storeDataPortscan(self,data):
		if self.mode == "module":
			if "portscan" not in State.moduleData:
				State.moduleData["portscan"] = {}
			if self.module_name not in State.moduleData["portscan"]:
				State.moduleData["portscan"][self.module_name] = {}
			for ip in data:
				State.moduleData["portscan"][self.module_name][ip] = data[ip]
		elif self.mode == "profile":
			if self.profile_tag != None:
				if self.profile_tag not in State.profileData:
					State.profileData[self.profile_tag] = {}
				if "portscan" not in State.profileData[self.profile_tag]:
					State.profileData[self.profile_tag]["portscan"] = {}
				if self.module_name != None:
					if self.module_name not in State.profileData[self.profile_tag]["portscan"]:
						State.profileData[self.profile_tag]["portscan"][self.module_name] = {}
					for ip in data:
						State.profileData[self.profile_tag]["portscan"][self.module_name][ip] = data[ip]
	
	def storeDataRegular(self,data):
		if self.mode == "module":
			if "regular" not in State.moduleData:
				State.moduleData["regular"] = {}
			if self.module_name not in State.moduleData["regular"]:
				State.moduleData["regular"][self.module_name] = {}
			for ip in data:
				State.moduleData["regular"][self.module_name][ip] = data[ip]
		elif self.mode == "profile":
			if self.profile_tag != None:
				if self.profile_tag not in State.profileData:
					State.profileData[self.profile_tag] = {}
				if self.profile_port != None:
					if "regular" not in State.profileData[self.profile_tag]:
						State.profileData[self.profile_tag]["regular"] = {}
					for ip in data:
						if ip not in State.profileData[self.profile_tag]["regular"]:
							State.profileData[self.profile_tag]["regular"][ip] = {}
						if self.profile_port not in State.profileData[self.profile_tag]["regular"][ip]:
							State.profileData[self.profile_tag]["regular"][ip][self.profile_port] = {}
						State.profileData[self.profile_tag]["regular"][ip][self.profile_port][self.module_name] = data[ip]
	
	@staticmethod
	def targets(val):
		out = []
		if val != None and type(val) == str:
			if bool(re.match(r'^([0-9]+\.){3}[0-9]+$',val)):
				out.append(val)
			elif bool(re.match(r'^([0-9]+\.){3}[0-9]+\/[0-9]+$',val)):
				for addr in netaddr.IPNetwork(val):
					out.append(str(addr))
			elif bool(re.match(r'^((([0-9]+\.){3}[0-9]+\,)+)(([0-9]+\.){3}[0-9]+)$',val)):
				out.extend(val.split(","))
		return out
