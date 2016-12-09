import os
import subprocess
from os import listdir
from os import path
from os import rename
from SystemLib import modify_System_Lib
import sys, getopt
import shutil, errno
def main(argv):

    # write logic to move class into working dir and do everything there


	folder = ''

	try:
		opts, args = getopt.getopt(argv, "hf:")
	except getopt.GetoptError as err:
		print('APEXC.py -f <folder>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print('APEXC.py -f <folder>')
			sys.exit()
		elif opt == '-f':
			folder = arg

        workingDir = "C:\\Users\\Amrita\\PycharmProjects\\workingDir\\"
        #check if workingDir is already present , delete it
        if(os.path.isdir(workingDir) == True):
                shutil.rmtree(workingDir)

        shutil.copytree(folder, workingDir)
        folder = workingDir

	for filename in listdir(workingDir):
		extension = path.splitext(filename)[1]
		if extension == '.cls':
                    newfile = filename.replace(extension, '.java')
                    os.rename(workingDir+'\\'+filename, workingDir+'\\'+newfile)

    # call object to java converter
    # call Modify System Lib to MfiflexSystem Lib
        for filename in listdir(workingDir):
            modify_System_Lib(filename, workingDir)

        file1 = "MfiflexSystem.java"
        file2 = "LoggingLevel.java"


        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\'+file1, workingDir+'\\'+file1)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\'+file2, workingDir + '\\'+file2)
    # call javac compiler
	cmd = "javac "+workingDir+"\*.java"
	proc = subprocess.Popen(cmd, shell=True)
	

if __name__ == "__main__":
	main(sys.argv[1:])

