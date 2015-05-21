import sys;
import os;
import re;
import glob;
import bisect;
import collections;

#author: Halima Olapade
#date: May 2015
#example output: format 'nodeID,node,month1,month2'

nodes = [];
resultDir = '/uniqNodes/';
resultFileN = ""

def parse(year, resultsPath, dirPath):
    global nodes;    
    global resultFileN;
    
    print "Beginning program to parse file and create node listings for nodes, ids and months of occurence\n"

    resultFileN = resultsPath + resultDir + year 
       
    try:
        os.remove(resultFileN);
    except OSError:
        pass;

    for num in range (0, 35):
        fileN = dirPath + "/"

        if num < 10:
            fileN += "uk-" + year + "-0" + str(num)
        else:
            fileN += "uk-" + year + "-" + str(num)
    
        #print "fileN:",fileN
        #continue
 
        with open(fileN, "r") as file:
            print("Current file: " + file.name)
        
            for line in file:
                args = line.split("\t");
                id1 = int(args[0])
                id2 = int(args[1].strip("\n"))

                #print id1,id2
        
                if not id1 in nodes:
                    bisect.insort(nodes, id1) 
                
                if not id2 in nodes:
                    bisect.insort(nodes, id2)    
            
    writeRecords();

def writeRecords():
    resultFile = open(resultFileN, "w");

    for id in nodes:
        resultFile.write(str(id) + "\n");
    resultFile.close();               

def main():
    if (not len(sys.argv) > 3):
        print ("Error: you must provide the year to pare, path to results dir containing \'uniqNodes\' directory and also a path to a directory containing ukDELIS edges files to read from.");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        arg3 = sys.argv[3];
        parse(arg1, arg2, arg3);


if __name__ == "__main__":
    main()
