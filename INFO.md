------------------------------------- <br/>
This tool intends to aid in exam by reducing painfull stuff.
<br/>
Commands: <br/>
- ls: list ccurrent menu options <br/>
- help: list Global menu options <br/>
- config get: list configuration option, there are a couple but easy to understand. <br/>
- config set: {{option}} value - define config options <br/>
<br/>
Note: config set HOSTIP {{youIP}}, make sure you set HOSTIP to the one on the network you are testing. <br/>
<br/>
Features: <br/>
- Buffer Overflow Helper <br/>
- Enumeration Automation Helper (Threaded): <br/>
- SSH User enum; <br/>
- SMTP VRFY + nmap scans (vuln,enum); <br/>
- DNS rECON; <br/>
- http dirsearch,nikto; <br/>
- SNMP onesixtyone + nmap scans (vuln,enum) <br/>
- 445 , smbmap,nbtscan, enum4linux, nmap (vuln,enum) <br/>
- https same as http; <br/>
- You can build your own modules following the standard structure of the above; <br/>
- File Sharing Helper (http,ftp,smb) <br/>

<br/>
The main goal is to allow the user to create their own enumeration by using python scripts. <br/>
Program is threaded so you can perform the above tasks simultaneously. <br/>
Program has a session awareness, all scans are stored in files/json on db/sessions/{{name}}. <br/>
<br/>
Enumeration Automation: <br/>
Relevant Classes: <br/>
	- /src/moddule.py Module <br/>
	- /src/modules/portscan/portscanner.py Portscanner (Specfic type of Module) <br/>
	- /src/profiles/profiler.py Profiler <br/>
Relevant Files: <br/>
	- tcp.tpl <br/>
	- tcp10k.tpl <br/>
	- udp.tpl <br/>
	(json structure to automate enumeration, user specifies a portscan module and specifies which modules run on specific ports. Modules only run if port is open. And it is a threaded application with the ability to limit) <br/>

Adding new Module: <br/>
 - Check /src/modules for module file structure examples. <br/>
 - Write your own; <br/> 
 - Add module entry in src/menus/module.py switcher_module variable following the examples. <br/>
 - Success you now have added a new custom Module! <br/>
<br/>
Data Filtering: <br/>
Global Cmds: <br/>
	- profiles (filters data from runned profiles, type "profiles help" for filter list, e.g profiles type=portscan) <br/>
	- modules (filters data from runned modules, type "modules help" for filter list, e.g modules type=regular) <br/>
	- services (filters data from runned portscan modules, either via manual or via tpl file, type "services help" for filter list, e.g services ip=127.0.0.1) <br/>
	- hosts (filters ips from global data, type "hosts help" e.g hosts module=Module_Ping) <br/> 
<br/>
NOTE: Read over the profile .tpl file, exisitng have dependencies on apt install seclists for path '/usr/share/seclists/Usernames/top-usernames-shortlist.txt'. <br/>
change the current profile template files or create your own. <br/>
<br/>
WIP.. 

