from src.modules.module import Module

class PortScanner(Module):

	def __init__(self):
		super().__init__()

	@staticmethod
	def getPorts(data):
		raise NotImplementedError

	@staticmethod
	def printData(data):
		raise NotImplementedError
