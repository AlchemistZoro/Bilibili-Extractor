import os

def getFileList(file_dir,ftype):
	lf=[]
	for root, dirs, files in os.walk(file_dir):
		for file in files:
			if file.split('.')[-1]==ftype:
				lf.append(file)
		return lf
        


def getBinaryFile(filename):
	f = open(filename, "rb")
	data = f.read()
	f.close()
	return data


