import http.server
import socketserver
import signal, sys


def signal_handler(sig, frame):
	sys.exit()

def httpserver(PORT=80):

	signal.signal(signal.SIGINT, signal_handler)

	Handler = http.server.SimpleHTTPRequestHandler
	with socketserver.TCPServer(("", PORT), Handler) as httpd:
		httpd.serve_forever()
