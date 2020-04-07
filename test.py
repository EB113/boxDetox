import os

#proc = os.popen("/bin/bash -c 'python3 "+ Config.PATH +"/3rd/dirsearch/dirsearch.py -u http://"+ ip +"/ -E -w /usr/share/wordlists/dirb/common.txt --json-report="+ Config.PATH +"/db/sessions/"+ Config.SESSID +"/tmp/dirsearch.json'")
#proc = os.popen("/bin/bash -c 'python3 /opt/oscpPWN/3rd/dirsearch/dirsearch.py -u http://10.11.1.8/ -E -w /usr/share/wordlists/dirb/common.txt --json-report=/opt/oscpPWN/dirsearch.json | grep -E \"^[^0-9].+\"'")
proc = os.popen("python3 /opt/oscpPWN/3rd/dirsearch/dirsearch.py -u http://10.11.1.8/ -E -w /usr/share/wordlists/dirb/common.txt --json-report=/opt/oscpPWN/dirsearch.json | grep -E '^\[([0-9]+\:){2}[0-9]+\]'")
print("python3 /opt/oscpPWN/3rd/dirsearch/dirsearch.py -u http://10.11.1.8/ -E -w /usr/share/wordlists/dirb/common.txt --json-report=/opt/oscpPWN/dirsearch.json | grep -E '^\[([0-9]+\:){2}[0-9]+\]'")
print(proc.read())
proc.close()
