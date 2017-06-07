import os
import sys

directory = sys.argv[1]
print directory
outputFileName = directory + "\\" + "analysis.csv"
outputFile = open(outputFileName,"wb+")
outputFile.write("problem name"+","+"slots-OBJ0"+","+"costs-OBJ1\n")
for root, dirs, files in os.walk(directory):
    #print files
    for file in files:
        if file.endswith('.sol'):
            print file
            tempfilename = directory + "\\" + file
            fileOpen =  open(tempfilename,"r")
            line = fileOpen.next()
            strings = line.split()
            print file,strings[0],strings[1]
            outputFile.write(file+","+strings[0]+","+strings[1]+"\n")
outputFile.close()