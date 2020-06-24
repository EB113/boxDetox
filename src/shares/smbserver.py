import sys,signal

from impacket import smbserver
from impacket.ntlm import compute_lmhash, compute_nthash


def signal_handler(sig, frame):
	sys.exit()

def smbServer(HOST="127.0.0.1",PORT="445",USER="user",PASS="user",SHAREPATH="/opt/oscpPWN/db/shares"):

    signal.signal(signal.SIGINT, signal_handler)
    server = smbserver.SimpleSMBServer(HOST, int(PORT))

    server.addShare("shares",SHAREPATH, "")
    server.setSMB2Support(True)

    # If a user was specified, let's add it to the credentials for the SMBServer. If no user is specified, anonymous
    # connections will be allowed
    lmhash = compute_lmhash(PASS)
    nthash = compute_nthash(PASS)

    #server.addCredential(USER, 0, lmhash, nthash)

    # Here you can set a custom SMB challenge in hex format
    # If empty defaults to '4141414141414141'
    # (remember: must be 16 hex bytes long)
    # e.g. server.setSMBChallenge('12345678abcdef00')
    server.setSMBChallenge('')

    # If you don't want log to stdout, comment the following line
    # If you want log dumped to a file, enter the filename
    #server.setLogFile('')

    # Rock and roll
    server.start()

