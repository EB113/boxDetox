import threading

class Module(threading.Thread):

	def __init__(self):
		self.flag = threading.Event()
	
	@staticmethod
	def validate(opt_dict):
		raise NotImplementedError
	
	@staticmethod
	def printData(data):
		raise NotImplementedError
