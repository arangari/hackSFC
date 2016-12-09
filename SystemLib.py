import os
import subprocess
from os import listdir
from os import path
from os import rename

import sys, getopt


def modify_System_Lib(filename, folder):
    fr = open(folder + '/' + filename, 'r')
    apex_content = fr.read()
    fr.close()
    apex_content = apex_content.replace('System.', 'MfiflexSystem.')
    apex_content = apex_content.replace('\'','\"')
    fw = open(folder + '/' + filename, 'w')
    fw.write(apex_content)
    fw.close()


def main(argv):
    folder = ''

    try:
        opts, args = getopt.getopt(argv, "hf:")
    except getopt.GetoptError as err:
        print('SystemLib.py -f <folder>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('SystemLib.py -f <folder>')
            sys.exit()
        elif opt == '-f':
            folder = arg

    for filename in listdir(folder):
        extension = path.splitext(filename)[1]
        if extension.endswith('java'):
            modify_System_Lib(filename, folder)


if __name__ == "__main__":
    main(sys.argv[1:])