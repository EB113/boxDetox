import sys,os,re
import clipboard

from ..miscellaneous.config import bcolors

def bof_badchars(cmd=None,state=None):
	out = ""
	outFormat = "c"
	if cmd != None and len(cmd) == 1:
		for i in range(0,256):
			out = out + "\\x" + format((ord(chr(i))), "x").zfill(2)
	elif len(cmd) == 2 or len(cmd) == 3:
		if len(cmd) == 3:
			outFormat = cmd[2]
		elif len(cmd) == 2 and cmd[1][0] != "\\":
			outFormat = cmd[1]
		out = ""
		badchars = cmd[1].split(r"\x")
		for i in range(0,256):
			tmp = format((ord(chr(i))), "x").zfill(2)
			if tmp not in badchars :
				out = out + "\\x" + tmp
	else:
		print("{}Usage: badchars [\\x00\\x0a...] [c | python]{}".format(bcolors.WARNING,bcolors.ENDC))
		return
	badcharcp = ""
	numChars = len(out)
	for i in range(0,numChars):
		if i % 64 == 0 and i != 0:
			badcharcp += "\"\n"
			badcharcp += "\""
		badcharcp += out[i]
	if outFormat == "c":
		badcharcp = "badchars =\n\"" + badcharcp + "\";\n"
	elif outFormat == "python":
		badcharcp = "badchars = (\n\"" + badcharcp + "\")\n"
	else:
		print("{}Invalid output format specified, defaulting to c\n(Accepted formats are \"c\" and \"python\"){}".format(bcolors.WARNING,bcolors.ENDC))
		badcharcp = "badchars =\n\"" + badcharcp + "\";\n"
	print("\n" + badcharcp)
	clipboard.copy(badcharcp)
	print("Number of characters: " + str(round(numChars/4)) + "\n")
	print("{}* Badchars copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_pattern(cmd=None,state=None):
	if len(cmd) == 2:
		# CHECK IF NUMBER
		patterncm = ("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l " + cmd[1])
		print(patterncm + "\n")
		patterncp = os.popen(patterncm).read()
		print(patterncp)
		clipboard.copy(patterncp)
		print("{}* Offset copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: pattern <length>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_offset(cmd=None,state=None):
	if len(cmd) == 2:
		# CHECK IF NUMBER
		offsetcm =("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q " + cmd[1])
		print(offsetcm + "\n")
		offsetcp = os.popen(offsetcm).read()
		print(offsetcp)
		offsetpp = os.popen(offsetcm + "|awk -F' ' '{print $6}'").read()
		clipboard.copy(offsetpp)
		print("{}* Offset copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: offset <pattern>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_lendian(cmd=None,state=None):
	if len(cmd) == 2:
		# CHECK IF ADDRESS
		if bool(re.match("^[0-9a-zA-Z]+$",cmd[1])):
			n=len(cmd[1])-2
			if n == 6 or n == 14:
				out=""
				while(n > -2):
					out+="\\x" + cmd[1][n]+cmd[1][n+1]
					n-=2
				print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,out))
				clipboard.copy(out)
				print("{}* Lendian address copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
			else:
				print("{}Wrong address format! Use 64bit or 32bit address.{}".format(bcolors.WARNING,bcolors.ENDC))
		else:
			print("{}Invalid Address!e.g:080414C3{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: lendian <address>{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_nasm(cmd=None):
	if len(cmd) == 1:
		# CHECK IF NUMBER
		os.system("/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb")
	else:
		print("{}Usage: nasm{}".format(bcolors.WARNING,bcolors.ENDC))

def bof_nops(cmd=None,state=None):
	num = 1
	if len(cmd) == 1:
		print("{}How many nops do you want?{}".format(bcolors.WARNING,bcolors.ENDC))
		num = int(sys.stdin.readline())
		print("\nHere ya go:\n")
		out = "\\x90" * num
		print(out + "\n")
		clipboard.copy(out)
		print("{}* Nops copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	elif len(cmd) == 2:
		num = int(cmd[1])
		out = "\\x90" * num
		print("\n" + out + "\n")
		clipboard.copy(out)
		print("{}* Nops copied to clipboard{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: nops number{}".format(bcolors.WARNING,bcolors.ENDC))


def bof_notes(cmd=None,state=None):
	if len(cmd) == 1:
		for item in switcher_notes.keys():
			print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,item))
	if len(cmd) == 2:
		if cmd[1] in switcher_notes.keys():
			for item in switcher_notes.get(cmd[1], ["Empty List!"]):
				print("{}[*] {}{}{}".format(bcolors.OKBLUE,bcolors.ENDC,bcolors.BOLD,item))
		else:
			print("{}Missing specified note!{}".format(bcolors.WARNING,bcolors.ENDC))
	else:
		print("{}Usage: notes <name|empty>{}".format(bcolors.WARNING,bcolors.ENDC))

switcher_notes = {
				"bof" : [r'!mona bytearray -b "\x00"',r'!mona compare -f bytearray.txt -a esp',r'!mona jmp -r esp -cpb "\x00"']
			}
