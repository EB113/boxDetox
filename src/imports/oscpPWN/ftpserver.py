import os,signal,sys

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def signal_handler(sig, frame):
    sys.exit()

def ftpserver(HOSTIP="127.0.0.1",PORT=21,USER="user",PASS="user"):
    signal.signal(signal.SIGINT, signal_handler)
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user(USER, PASS, '.', perm='elradfmwMT')
    #authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (HOSTIP, PORT)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 2
    server.max_cons_per_ip = 2

    # start ftp server
    server.serve_forever()
