from src.module.module import Module

class PortScanner(Module):

	def __init__(self,opt_dict,save_location,module_name,profile_tag=None,profile_port=None):
		super().__init__(opt_dict,save_location,module_name,profile_tag,profile_port)

	@staticmethod
	def getPorts(data):
		raise NotImplementedError
