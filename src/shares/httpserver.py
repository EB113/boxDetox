import http.server
import socketserver
import signal, sys


def signal_handler(sig, frame):
	sys.exit()

def httpServer(HOSTIP="127.0.0.1",PORT="80"):

	signal.signal(signal.SIGINT, signal_handler)

	Handler = http.server.SimpleHTTPRequestHandler
	with socketserver.TCPServer((HOSTIP, int(PORT)), Handler) as httpd:
		httpd.serve_forever()
