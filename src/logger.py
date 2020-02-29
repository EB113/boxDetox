import traceback,socket

from _thread import *
import threading

import pyfiglet

from src.miscellaneous.config import bcolors,Config

class ClientThread(threading.Thread):
	
	def __init__(self,conn,print_lock):
		threading.Thread.__init__(self)
		self.conn = conn
		self.print_lock = print_lock

	def run(self):
		self.print_lock.acquire()
		while True:
			data = self.conn.recv(1024)
			if not data:
				self.print_lock.release()
				break
			print(data.decode())
		self.conn.close()

print("{}{}{}".format(bcolors.HEADER,pyfiglet.figlet_format("oscpPWN"),bcolors.ENDC))

try:
	print_lock = threading.Lock()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((Config.LOGGERIP,int(Config.LOGGERPORT)))

		s.listen(5)
		while True:
			conn,addr = s.accept()
			newclient = ClientThread(conn,print_lock)
			newclient.start()
except Exception as e:
	print("{}".format(e))
	print("{}".format(traceback.print_exc()))
