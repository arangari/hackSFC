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


        workingDir = "C:\\Users\\Amrita\\PycharmProjects\\workingDir\\"

#check if workingDir is already present , delete it

        if(os.path.isdir(workingDir) == True):
            shutil.rmtree(workingDir)

        shutil.copytree(folder+'\\classes', workingDir)

    # call object to java converter
        objDir = folder + '\\objects'
        print('Object dir :' + objDir);
        createPoJoForSFObject(objDir, workingDir)

	for filename in listdir(workingDir):
		extension = path.splitext(filename)[1]
		if extension == '.cls':
                    newfile = filename.replace(extension, '.java')
                    os.rename(workingDir+'\\'+filename, workingDir+'\\'+newfile)


        # call Modify System Lib to MfiflexSystem Lib
        for filename in listdir(workingDir):
            modify_System_Lib(filename, workingDir)

        file1 = "MfiflexSystem.java"
        file2 = "LoggingLevel.java"
        file3 = "Date.java"
        file4 = "ID.java"
        file5 = "DateTime.java"
        file6 = "sObject.java"
        file7 = "Database.java"
        file8 = "Savepoint.java"
        file9 = "DMLException.java"
        file10 = "mfiflexUtil.java"

        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\'+file1, workingDir+'\\'+file1)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\'+file2, workingDir + '\\'+file2)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file3, workingDir + '\\' + file3)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file4, workingDir + '\\' + file4)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file5, workingDir + '\\' + file5)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file6, workingDir + '\\' + file6)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file7, workingDir + '\\' + file7)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file8, workingDir + '\\' + file8)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file9, workingDir + '\\' + file9)
        shutil.copy('C:\\Users\\Amrita\\PycharmProjects\\APEXC\\src\\' + file10, workingDir + '\\' + file10)
    # call javac compiler
	cmd = "javac "+workingDir+"\*.java"
	proc = subprocess.Popen(cmd, shell=True)
	

if __name__ == "__main__":
	main(sys.argv[1:])

