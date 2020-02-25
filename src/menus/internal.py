#from ..imports.impacket import smbserver

def share_smb():
	return
def share_ftp():
	return
def share_http():
	return
def share_powershell():
	return
def share_vbscript():
	return

switcher_share = {"smb":share_smb,"ftp":share_ftp,"http":share_http,"powershell":share_powershell,"vbscript":share_vbscript}


def internal_share(cmd=None,state=None):

	switcher_share.get(cmd[0],"Invalid!")(cmd,state)
