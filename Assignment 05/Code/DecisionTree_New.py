import csv
import sys
from collections import defaultdict

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]


columns = defaultdict(list) # each value in each column is appended to a list

with open(input_file_name) as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    rowcounter = 0;
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k
        

                    
                                
            
                
        
        #outputFile.write(rowcounter
        rowcounter += 1
        
    #outputFile.write(range(0,rowcounter)
    #outputFile.write(rowcounter
    outputFile = open(output_file_name,"wb")
    
    for counter in range(0,rowcounter):
        if(float(columns['plum'][counter])<10.02):
            if(float(columns['silver'][counter])<0.1):
                if(float(columns['chocolate'][counter])<1.58):
                    if(float(columns['blue'][counter])<0.17):
                        if(float(columns['aquamarine'][counter])<9.5):
                            outputFile.write("sparrow\n")
                        else:
                            outputFile.write("goose\n")
                    else:
                        if(float(columns['green'][counter])<0.07):
                            outputFile.write("albatross\n")
                        else:
                            outputFile.write("roadrunner\n")
                else:
                    if(float(columns['plum'][counter])<9.86):
                        if(float(columns['gray'][counter])<3660):
                            if(float(columns['maroon'][counter])<2.04):
                                outputFile.write("swan\n")
                            else:
                                outputFile.write("goose\n")
                        else:
                            if(float(columns['black'][counter])<0.08):
                                outputFile.write("pigeon\n")
                            else:
                                outputFile.write("swan\n")
                    else:
                        if(float(columns['almond'][counter])<2789.56):
                            outputFile.write("chickadee\n")
                        else:
                            outputFile.write("robin\n")
            else:
                if(float(columns['seagreen'][counter])<0.62):
                    if(float(columns['brown'][counter])<0.64):
                        outputFile.write("goose\n")
                    else:
                        if(float(columns['almond'][counter])<1980.69):
                            outputFile.write("petrel\n")
                        else:
                            outputFile.write("sparrow\n")
                else:
                    if(float(columns['seagreen'][counter])>=0.62):
                        if(float(columns['plum'][counter])<8.42):
                            if(float(columns['blue'][counter])<0.61):
                                outputFile.write("chickadee\n")
                            else:
                                if(float(columns['gray'][counter])<128):
                                    outputFile.write("goose\n")
                                else:
                                    outputFile.write("chickadee\n")
                        else:
                            if(float(columns['red'][counter])<0.01):
                                outputFile.write("chickadee\n")
                            else:
                                if(float(columns['almond'][counter])<751.93):
                                    outputFile.write("robin\n")
                                else:
                                    outputFile.write("plover\n")
        else:
            if(float(columns['aqua'][counter])<0.37):
                if(float(columns['purple'][counter])<9):
                    if(float(columns['maroon'][counter])<1.65):
                        outputFile.write("parrot\n")
                    else:
                        if(float(columns['green'][counter])<0.2):
                            outputFile.write("plover\n")
                        else:
                            if(float(columns['copper'][counter])<901.5):
                                outputFile.write("falcon\n")
                            else:
                                outputFile.write("chickadee\n")
                else:
                    if(float(columns['almond'][counter])<341.11):
                        if(float(columns['aquamarine'][counter])<37):
                            outputFile.write("chickadee\n")
                        else:
                            outputFile.write("duck\n")
                    else:
                        if(float(columns['gray'][counter])<132.5):
                            if(float(columns['purple'][counter])<35.08):
                                outputFile.write("falcon\n")
                            else:
                                outputFile.write("parrot\n")
                        else:
                            outputFile.write("roadrunner\n")
            else:
                if(float(columns['indigo'][counter])<6.73):
                    if(float(columns['lime'][counter])<0.11):
                        if(float(columns['copper'][counter])<39251):
                            outputFile.write("osprey\n")
                        else:
                            outputFile.write("robin\n")
                    else:
                        outputFile.write("chickadee\n")
                else:
                    if(float(columns['gold'][counter])<0.33):
                        outputFile.write("goose\n")
                    else:
                        outputFile.write("heron\n")
                        
    outputFile.close()   
f.close()    
                    
                                
                        
                        
                   
