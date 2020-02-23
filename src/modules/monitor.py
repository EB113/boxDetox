import threading
import queue
import time

from ..menus.commons import State

class Monitor(threading.Thread):

	def __init__(self,queue):
		threading.Thread.__init__(self)
		self.flag = threading.Event()
		self.procList = []
		self.reqList = queue

	# Should I clean waiting threads in the queue??
	def shutdown(self):
		for proc in self.procList:
			proc[1].flag.set()
		for proc in self.procList:
			proc[1].join(timeout=60)

	def run(self):
		while not self.flag.is_set():
			# Check for finished tasks
			for proc in self.procList[:]:
				if not proc[1].isAlive():
					print("Task {} Finished!".format(proc[0]))
					self.procList.remove(proc)
			# Check for new tasks
			try:
				req = self.reqList.get_nowait()
				req[1].start()
				self.procList.append(req)
			except:
				pass

			time.sleep(1)
		self.shutdown()
		return
