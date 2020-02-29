import os



for root,dirs,files in os.walk("/opt/oscpPWN/src/modules"):
	print(root)
	print(dirs)
	print(files)
