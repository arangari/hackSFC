import os
import subprocess
from os import listdir
from os import path
from os import rename

import sys, getopt
import re

def modify_System_Lib(filename, folder):
    fr = open(folder + '/' + filename, 'r')
    apex_content = fr.read()
    fr.close()
    apex_content = apex_content.replace('System.Debug', 'MfiflexSystem.Debug')
    apex_content = apex_content.replace('System.now', 'MfiflexSystem.now')
    apex_content = apex_content.replace('System.debug', 'MfiflexSystem.Debug')
    apex_content = apex_content.replace('system.debug', 'MfiflexSystem.Debug')
    apex_content = apex_content.replace('System.assert', 'assert')
    apex_content = apex_content.replace('\"','\\"')
    apex_content = apex_content.replace('\'','\"')
    apex_content = apex_content.replace('global', 'public')
    apex_content = apex_content.replace('override', '')
    apex_content = apex_content.replace('instanceOf', 'instanceof')
    apex_content = apex_content.replace('database', 'Database')
    apex_content = apex_content.replace('logginglevel.error', 'LoggingLevel.ERROR')
    apex_content = apex_content.replace('Interface', 'interface')
    apex_content = apex_content.replace('virtual', '')
    apex_content = apex_content.replace('with', '')
    apex_content = apex_content.replace('sharing', '')
    apex_content = apex_content.replace('math', 'Math')
    apex_content = apex_content.replace('date', 'Date')
    apex_content = apex_content.replace('Decimal', 'Integer')
    apex_content = apex_content.replace('setScale', 'valueOf')
    apex_content = apex_content.replace(' public Integer compareTo','@Override \n public int compareTo')
    apex_content = apex_content.replace('private class DiagnosticEntry','private static class DiagnosticEntry')
    #apex_content = apex_content.replace('PageReference', 'void')
    apex_content = apex_content.replace('testMethod', '')
    #apex_content = apex_content.replace('{get; set;}', ';')
    apex_content = apex_content.replace('new List', 'new ArrayList')
    soql_regex1 = r"(\s*\[[\w\s,.=:'\(\)\"\d+]*\sFROM\s([\w\d_]*)[\w\s,.=:'\(\)\"\d+]*\])"
    #soql_regex2 = r" new \2 ();\n/* \1 */"
    soql_regex2 = r" null\n/* \1 */"

    apex_content = re.sub(soql_regex1, soql_regex2, apex_content, flags=re.IGNORECASE)
    #apex_content = apex_content.replace('[S','null/*');
    #apex_content = apex_content.replace('[s', 'null/*');
    #apex_content = apex_content.replace('];','*/;');
    #apex_content = apex_content.replace('0*/;', '0];');
    #apex_content = apex_content.replace('10];', '*/;');
    apex_content = apex_content.replace('@future', '//@future');
    apex_content = apex_content.replace('getStackTraceString','getStackTrace');
    apex_content = apex_content.replace('getLineNumber', 'getStackTrace');
    apex_content = apex_content.replace('getTypeName', 'getStackTrace');
    apex_content = re.sub("\{[\w\s]*get\s*;[\w\s]*set\s*;\s*\}", ";", apex_content)

    fw = open(folder + '/' + filename, 'w')
    fw.write('import java.util.*;\n')
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