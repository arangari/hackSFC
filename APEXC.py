import os
import subprocess
from os import listdir
from os import path
from os import rename
from SystemLib import modify_System_Lib
from SFObjectParser import createPoJoForSFObject
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
                print('process.py -f <folder>')
                sys.exit()
            elif opt == '-f':
                folder = arg


        workingDir = os.path.join(folder, 'workingDir')
    #"C:\\Users\\Amrita\\PycharmProjects\\workingDir\\"

#check if workingDir is already present , delete it

        if(os.path.isdir(workingDir) == True):
            shutil.rmtree(workingDir)

        shutil.copytree(os.path.join(folder, 'classes'), workingDir)

    # call object to java converter
        objDir = os.path.join(folder, 'objects')
        print('Object dir :' + objDir);
        createPoJoForSFObject(objDir, workingDir)

	for filename in listdir(workingDir):
		extension = path.splitext(filename)[1]
		if extension == '.cls':
                    newfile = filename.replace(extension, '.java')
                    os.rename(os.path.join(workingDir, filename), os.path.join(workingDir, newfile))


        # call Modify System Lib to MfiflexSystem Lib
        for filename in listdir(workingDir):
            modify_System_Lib(filename, workingDir)

        libFolder = os.path.join(folder, 'lib');
        for file in listdir(libFolder):
            shutil.copy(os.path.join(libFolder, file), os.path.join(workingDir, file))
        #shutil.copytree(libFolder, workingDir)

    # call javac compiler
	cmd = "javac "+workingDir+"\*.java"
	proc = subprocess.call(cmd, shell=True)
#subprocess.subprocess.Popen(cmd, shell=True)
	

if __name__ == "__main__":
	main(sys.argv[1:])

