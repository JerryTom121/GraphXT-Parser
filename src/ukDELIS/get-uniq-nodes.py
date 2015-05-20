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

def parse(resultsPath, dirPath):
    global nodes;    
    global resultFileN;
    
    print "Beginning program to parse file and create node listings for nodes, ids and months of occurence\n"

    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(dirPath, '*')):
        r = re.compile('uk-(.*?).edges')
        m = r.search(fileN)
        timeInt = ""        

        if m:
            timeInt = m.group(1).replace("-", "")
        else:
            print "Found a file that is not an edges file:", fileN
            continue;

        resultFileN = resultsPath + resultDir + timeInt 
        
        try:
            os.remove(resultFileN);
        except OSError:
            pass;
        
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
            del nodes[:]                

def writeRecords():
    resultFile = open(resultFileN, "w");

    for id in nodes:
        resultFile.write(str(id) + "\n");
    resultFile.close();               

def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide path to results dir containing \'uniqNodes\' directory and also a path to a directory containing ukDELIS edges files to read from.");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        parse(arg1, arg2);


if __name__ == "__main__":
    main()
