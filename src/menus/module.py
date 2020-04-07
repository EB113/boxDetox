import queue

from src.miscellaneous.config import bcolors
from src.menus.commons import State

def module_run(cmd=None):
	if State.module_class.validate(State.env_option):
		if not State.procs.full():
			State.procs.put((State.module_state,State.module_class(State.env_option,"module",State.module_class.getName())))
		else:
			print("{}Too many module tasks!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Wrong options! ToDo show option example forced class from Super.{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_get(cmd=None):
	if len(cmd) == 1:
		print("{}Module options:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in State.module_class.opt.keys():
			val = State.env_option.get(option)
			if val is None:
				print("{}[*] {}{}{} --> None".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option))
			else:
				print("{}[*] {}{}{} --> {}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,option,val))
	else:
		print("{}Usage: get{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_set(cmd=None):
	if len(cmd) == 3:
		for option in State.module_class.opt.keys():
			if cmd[1] == option:
				State.env_option[cmd[1]] = cmd[2]
	else:
		print("{}Usage: set <option> <value>{}".format(bcolors.WARNING,bcolors.ENDC))
	return

switcher_module = {
	"modules/http/dirsearch":"Module_HTTP_dirsearch",
	"modules/http/dirb":"Module_HTTP_dirb",
	"modules/http/nikto":"Module_HTTP_nikto",
	"modules/smb/smbmap":"Module_SMB_smbmap",
	"modules/smb/enum4linux":"Module_SMB_enum4linux",
	"modules/smb/nbtscan":"Module_SMB_nbtscan",
	"modules/smb/nmap_vuln":"Module_SMB_nmapvuln",
	"modules/smb/nmap_enum":"Module_SMB_nmapenum",
	"modules/smtp/nmap_vuln":"Module_SMTP_nmapvuln",
	"modules/smtp/nmap_enum":"Module_SMTP_nmapenum",
	"modules/smtp/smtpvrfy":"Module_SMTP_smtpvrfy",
	"modules/ping":"Module_Ping",
	"modules/portscan/tcpcommon":"Module_SCAN_TCPCommon"
	,"modules/portscan/udpcommon":"Module_SCAN_UDPCommon"
	}
