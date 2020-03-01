import threading
import re

class Module(threading.Thread):

	def __init__(self):
		self.flag = threading.Event()
	
	@staticmethod
	def validate(opt_dict):
		raise NotImplementedError
	
	@staticmethod
	def printData(data,conn=None):
		raise NotImplementedError

	def storeData(self,data):
		raise NotImplementedError
	
	@staticmethod
	def targets(val):
		out = []
		if val != None and type(val) == str:
			if bool(re.match(r'^([0-9]+\.){3}[0-9]+$',val)):
				out.append(val)
			elif bool(re.match(r'^([0-9]+\.){3}[0-9]+\/[0-9]+$',val)):
				for addr in netaddr.IPNetwork(val):
					out.append(str(addr))
		return out
