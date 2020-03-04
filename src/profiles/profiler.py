import traceback,threading
import time,os
import netaddr,re
from importlib import import_module

from src.miscellaneous.config import Config

# Change everything to try except, get rid of boolean error check format

def validate_module(module,variables):
	if type(module) == str and os.path.isfile(Config.PATH + "/src/" + module + ".py"):
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

def validate_generic(val):
	if type(val) == dict:
		for k,v in val.items():
			if not validate_module(k,v):
				return False
	else:
		return False
	return True

class Profiler(threading.Thread):

	switcher_static  = {"tag":validate_tag, "globals":validate_variables, "portscan":validate_portscan, "ports":validate_ports}
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
		return out

	# Have a look at the best way to forcefully kill a child process
	def run(self):
		try:
			if "OUTFILE" in self.tpl["globals"]:
				path = self.tpl["globals"]["outfile"]
			else:
				path = Config.PATH + "/db/sessions/" + Config.SESSID + "/profiles/" + self.tpl["tag"]
			
			try:
				os.mkdir(path)
			except FileExistsError:
				pass

			portscan = list(self.tpl["portscan"])[0]
			("src/" + portscan).replace("/",".")

			portscan_module = import_module(("src/" + portscan).replace("/","."))

			lst = self.targets(self.tpl["globals"]["target"])
			for ip in lst:
				path_updated = path + "/" + ip
				try:
					os.mkdir(path_updated)
				except FileExistsError:
					pass
				self.tpl["portscan"][portscan]["outfile"] = path_updated
				try:
					portscan_class = getattr(portscan_module, self.tpl["portscan"][portscan]["name"])
					scanner = portscan_class({**self.tpl["globals"],**self.tpl["portscan"][portscan]},"profile",portscan_class.getName(),self.tpl["tag"])
					scanner.start()
					scanner.join()
				except Exception as e:
					print("{}".format(e))
					print("{}".format(traceback.print_exc()))
					print("Error Portscan!")
					return
				
				procList = []
				timeout_counter = 0

				try:
					for port in portscan_class.getPorts(self.tpl["tag"],ip):
						path_updated = path_updated + "/" + port
						try:
							os.mkdir(path_updated)
						except FileExistsError:
							pass
						if port in self.tpl["ports"]:
							for name,variables in self.tpl["ports"][port].items():
								# QUEUE for Threads
								while len(procList) >= Config.MAXPROFILES:
									if timeout_counter > Config.PROFILETIMEOUT:
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
