import traceback,threading
import time,os
import netaddr,re
from importlib import import_module

from src.miscellaneous.config import Config

# Change everything to try except, get rid of boolean error check format

def validate_module(module,variables):
	if type(module) == str and os.path.isfile(Config.CONFIG['GENERAL']['PATH'] + "/src/" + module + ".py"):
		if not validate_variables(variables):
			return False
		return True
	else:
		# Send Error
		return False

def validate_tag(val):
	if type(val) == str and not os.path.isfile(val):
		return True
	else:
		# Send Error
		return False

def validate_variables(val):
	if type(val) == dict:
		for k,v in val.items():
			if type(k) != str or (type(v) != str and type(v) != int):
				return False
	else:
		return False
	return True

def validate_portscan(val):
	if type(val) == dict:
		for k,v in val.items():
			if not validate_module(k,v):
				return False
	else:
		return False
	return True

def validate_ports(val):
	for k,v in val.items():
		try:
			int(k)
		except:
			# Send Error, print in menu.py
			print("Not Integer!")
			return False
		if type(v) == dict:
			for k1,v1 in v.items():
				if not validate_module(k1,v1):
					return False
		else:
			return False
	return True

def validate_services(val):
	for k,v in val.items():
		#	Add More Services
		if type(k) == str and k in ["http","https","ftp","snmp","ajp13","pop3","imap"]:
			if type(v) == dict:
				for k1,v1 in v.items():
					if not validate_module(k1,v1):
						return False
		else:
			# Send Error, print in menu.py
			print("Not String!")
			return False
	return True

def validate_generic(val):
	if type(val) == dict:
		for k,v in val.items():
			if not validate_module(k,v):
				return False
	else:
		return False
	return True

class Profiler(threading.Thread):

	switcher_static  = {"tag":validate_tag, "globals":validate_variables, "portscan":validate_portscan, "ports":validate_ports, "services":validate_services}
	switcher_dynamic = {"generic":validate_generic}

	def __init__(self,json):
		threading.Thread.__init__(self)
		self.flag = threading.Event()
		self.tpl = json

	def validate(json):
		for elem in Profiler.switcher_static:
			if elem in json:
				if not Profiler.switcher_static[elem](json[elem]):
					return False
			else:
				return False
		for elem in Profiler.switcher_dynamic:
			if elem in json:
				if not Profiler.switcher_dynamic[elem](json[elem]):
					return False
		return True

	# Make this global for every module
	def targets(self,val=None):
		out = []
		if bool(re.match(r'^([0-9]+\.){3}[0-9]+$',val)):
			out.append(val)
		elif bool(re.match(r'^([0-9]+\.){3}[0-9]+\/[0-9]+$',val)):
			for addr in netaddr.IPNetwork(val):
				out.append(str(addr))
		elif bool(re.match(r'^([0-9]+\.){3}[0-9]+\-[0-9]+$',val)): #todo x.x.x.x-y
			for addr in netaddr.IPNetwork(val):
				out.append(str(addr))
		elif bool(re.match(r'^((([0-9]+\.){3}[0-9]+\,)+)(([0-9]+\.){3}[0-9]+)$',val)):
				out.extend(val.split(","))
		return out

	# Have a look at the best way to forcefully kill a child process
	def run(self):
		try:
			if "OUTFILE" in self.tpl["globals"]:
				path = self.tpl["globals"]["outfile"]
			else:
				path = Config.CONFIG['GENERAL']['PATH'] + "/db/sessions/" + Config.CONFIG['GENERAL']['SESSID'] + "/profile/" + self.tpl["tag"]
			
			try:
				os.mkdir(path)
			except FileExistsError:
				pass

			portscan_paths = []
			portscan_modules = []
			for path_ in list(self.tpl["portscan"]):
				portscan_paths.append(path_)
				portscan_modules.append(import_module(("src/" + path_).replace("/",".")))

			lst = self.targets(self.tpl["globals"]["target"])
			for ip in lst:
				self.tpl["globals"]["target"] = ip
				path_updated = path + "/" + ip
				try:
					os.mkdir(path_updated)
				except FileExistsError:
					pass
				try:
					portscan_classes = []
					for path_,module in zip(portscan_paths,portscan_modules):
						self.tpl["portscan"][path_]["outfile"] = path_updated
						portscan_class = getattr(module, self.tpl["portscan"][path_]["name"])
						portscan_classes.append(portscan_class)
						scanner = portscan_class({**self.tpl["globals"],**self.tpl["portscan"][path_]},"profile",portscan_class.getName(),self.tpl["tag"])
						scanner.start()
						scanner.join()
				except Exception as e:
					print("{}".format(e))
					print("{}".format(traceback.print_exc()))
					print("Error Portscan!")
					return
				
				iterDitc = {}
				procList = []
				timeout_counter = 0

				try:
					# [(port,service)]
					tuples = []
					for portscan_class in portscan_classes:
						tuples.extend(portscan_class.getPortsServices(self.tpl["tag"],ip))

					for port,service in tuples:
						path_updated = path_updated + "/" + port
						if port in self.tpl["ports"] or service in self.tpl["services"]:
							try:
								os.mkdir(path_updated)
							except FileExistsError:
								pass

							if port in self.tpl["ports"]:
								iterDict = self.tpl["ports"][port]
							else:
								iterDict = self.tpl["services"][service]

							for name,variables in iterDict.items():
								# QUEUE for Threads
								while len(procList) >= Config.CONFIG['CONCURRENCY']['MAXPROFILES']:
									if timeout_counter > Config.CONFIG['CONCURRENCY']['PROFILETIMEOUT']:
										raise Exception("Profile Timeout!")
									timeout_counter = timeout_counter + 1
									time.sleep(timeout_counter)
									for proc in procList[:]:
										if not proc.isAlive():
											procList.remove(proc)
								timeout_counter = 0

								if not self.flag.is_set():
									variables["outfile"] = path_updated
									module = ("src/" + name).replace("/",".")
									imported_module = import_module(module)
									regular_class = getattr(imported_module, variables["name"])
									regular = regular_class({**self.tpl["globals"],**variables},"profile",regular_class.getName(),self.tpl["tag"],port)
									regular.start()
									procList.append(regular)
						path_updated = path_updated[:-(len(port)+1)]

				except Exception as e:
					print("{}".format(e))
					print("{}".format(traceback.print_exc()))
					print("Error Running module bla!")

		except Exception as e:
			print("{}".format(e))
			print("{}".format(traceback.print_exc()))
			print("Profile Setup failed!")
		#self.shutdown()
		return
