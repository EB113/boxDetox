import queue

from src.miscellaneous.config import bcolors
from src.menus.commons import State

def module_run(cmd=None, conn=None):
	if State.module_class.validate(State.env_option):
		if not State.procs.full():
			State.procs.put((State.module_state,State.module_class(State.env_option,"module",State.module_class.getName())))
		else:
			print("{}Too many module tasks!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Wrong options! Type 'get' for options information.{}".format(bcolors.WARNING,bcolors.ENDC))
	return

def module_get(cmd=None):
	if len(cmd) == 1:
		print("{}Module options:{}".format(bcolors.WARNING,bcolors.ENDC))
		for option in State.module_class.opt_static.keys():
			val = State.env_option.get(option)
			if val is None:
				print("{}[*] {}{}{} --> None".format(bcolors.OKGREEN,bcolors.ENDC,bcolors.BOLD,option))
			else:
				print("{}[*] {}{}{} --> {}".format(bcolors.OKGREEN,bcolors.ENDC,bcolors.BOLD,option,val))
		for option in State.module_class.opt_dynamic.keys():
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
		for option in State.module_class.opt_static.keys():
			if cmd[1] == option:
				State.env_option[cmd[1]] = cmd[2]
		for option in State.module_class.opt_dynamic.keys():
			if cmd[1] == option:
				State.env_option[cmd[1]] = cmd[2]
	else:
		print("{}Usage: set <option> <value>{}".format(bcolors.WARNING,bcolors.ENDC))
	return

switcher_module = {
	"module/nfs/nmap":"Module_NFS_nmap",
	"module/imap/nmap":"Module_IMAP_nmap",
	"module/pop3/nmap":"Module_POP3_nmap",
	"module/tftp/nmap":"Module_TFTP_nmap",
	"module/ajp/nmap":"Module_AJP_nmap",
	"module/ftp/nmap":"Module_FTP_nmap",
	"module/http/dirsearch":"Module_HTTP_dirsearch",
	"module/http/dirb":"Module_HTTP_dirb",
	"module/http/nikto":"Module_HTTP_nikto",
	"module/smb/smbmap":"Module_SMB_smbmap",
	"module/smb/enum4linux":"Module_SMB_enum4linux",
	"module/smb/nbtscan":"Module_SMB_nbtscan",
	"module/smb/nmap_vuln":"Module_SMB_nmapvuln",
	"module/smb/nmap_enum":"Module_SMB_nmapenum",
	"module/smtp/nmap_vuln":"Module_SMTP_nmapvuln",
	"module/smtp/nmap_enum":"Module_SMTP_nmapenum",
	"module/smtp/smtpvrfy":"Module_SMTP_VRFY",
	"module/ssh/userenum":"Module_SSH_userenum",
	"module/snmp/onesixtyone":"Module_SNMP_onesixtyone",
	"module/dns/dnsrecon":"Module_DNS_dnsrecon",
	"module/icmp/ping":"Module_ICMP_Ping",
	"module/portscan/tcp":"Module_SCAN_TCP",
	"module/portscan/udp":"Module_SCAN_UDP"
	}
