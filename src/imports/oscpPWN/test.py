import os, signal
import time

from ..menus.commons import State



pid = os.fork()

if pid:
	State.share_state["http"]["status"] = True
	State.share_state["http"]["pid"] = pid

	time.sleep(10)
	os.kill(State.share_state["http"]["pid"], signal.SIGINT)
	
	State.share_state["http"]["status"] = False
	State.share_state["http"]["pid"] = 0
else:
	print("Process ID:{}".format(os.getpid()))
	os.system("python3.7 httpserver.py")
