-------------------------------------
This tool intends to aid in exam by reducing painfull stuff.

Commands:
	- ls - list ccurrent menu options
	- help - list Global menu options
	- config get - list configuration option, there are a couple but easy to understand.
	- config set {{option}} value - define config options
	
	Note: config set HOSTIP {{youIP}}, make sure you set HOSTIP to the one on the network you are testing.

Features:
	- Buffer Overflow Helper
	- Enumeration Automation Helper (Threaded):
		- SSH User enum;
		- SMTP VRFY + nmap scans (vuln,enum);
		- DNS rECON;
		- http dirsearch,nikto;
		- SNMP onesixtyone + nmap scans (vuln,enum)
		- 445 , smbmap,nbtscan, enum4linux, nmap (vuln,enum)
		- https same as http;
		- You can build your own modules following the standard structure of the above;
	- File Sharing Helper (http,ftp,smb)

The main goal is to allow the user to create their own enumeration by using python scripts.
Program is threaded so you can perform the above tasks simultaneously.
Program has a session awareness, all scans are stored in files/json on db/sessions/{{name}}.

Enumeration Automation:
Relevant Classes:
	- /src/moddule.py Module
	- /src/modules/portscan/portscanner.py Portscanner (Specfic type of Module)
	- /src/profiles/profiler.py Profiler
Relevant Files:
	- tcp.tpl
	- tcp10k.tpl
	- udp.tpl
	(json structure to automate enumeration, user specifies a portscan module and specifies which modules run on specific ports. Modules only run if port is open. And it is a threaded application with the ability to limit)

Adding new Module:
 - Check /src/modules for module file structure examples.
 - Write your own;
 - Add module entry in src/menus/module.py switcher_module variable following the examples.
 - Success you now have added a new custom Module!

Data Filtering:
Global Cmds:
	- profiles (filters data from runned profiles, type "profiles help" for filter list, e.g profiles type=portscan)
	- modules (filters data from runned modules, type "modules help" for filter list, e.g modules type=regular)
	- services (filters data from runned portscan modules, either via manual or via tpl file, type "services help" for filter list, e.g services ip=127.0.0.1)
	- hosts (filters ips from global data, type "hosts help" e.g hosts module=Module_Ping)

NOTE: Read over the profile .tpl file, exisitng have dependencies on apt install seclists for path '/usr/share/seclists/Usernames/top-usernames-shortlist.txt'.
change the current profile template files or create your own.

WIP..
