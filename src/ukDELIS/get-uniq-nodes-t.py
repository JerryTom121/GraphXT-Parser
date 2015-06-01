import sys;
import os;
import re;
import traceback;
import threading;
from sortedcontainers import SortedDict;

#author: Halima Olapade
#date: May 2015
#example output: format 'nodeID,node,month1,month2'

nodes = SortedDict();
curIndex = 0;
resultDir = '/uniqNodes/';
resultFileN = ""
year = ""
dirPath = ""

newFileLock = threading.Lock()
writeId = threading.Lock()
threads = []

class ParseThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print "Starting " + self.name
       
        try: 
            newFileLock.acquire()
            fileP = getFilePath()
            newFileLock.release()

            while(fileP is not None):
                findIds(fileP)

                newFileLock.acquire()
                fileP = getFilePath()
                newFileLock.release()

            print "Exiting " + self.name
        except Exception:
            print traceback.format_exc()
            sys.exit(1)     


def getFilePath():
    global curIndex;
    filePath = dirPath + "/"
    
    if curIndex < 35: 
        if curIndex < 10:   
            filePath += "uk-" + year + "-0" + str(curIndex)
        else:
            filePath += "uk-" + year + "-" + str(curIndex)  
        curIndex += 1
    else:
        return None

    return filePath

def findIds(fileN):
    global nodes; 
    with open(fileN, "r") as file:
        print("Current file: " + file.name)
        
        for line in file:
            args = line.split("\t");
            id1 = int(args[0])
            id2 = int(args[1].strip("\n"))

            idsToWrite = []
            #print id1,id2
        
            if not id1 in nodes:
                idsToWrite.append(id1)
                
            if not id2 in nodes:
                idsToWrite.append(id2) 

            #add new ids to dict 
            if len(idsToWrite) == 0:
                continue;
            elif len(idsToWrite) == 1:
                writeId.acquire()
                nodes.update({idsToWrite[0] : 1}) 
                writeId.release()
            elif len(idsToWrite) == 2:
                writeId.acquire()
                nodes.update({idsToWrite[0] : 1}) 
                nodes.update({idsToWrite[1] : 1})
                writeId.release()  

def writeRecords(nodesDict):
    resultFile = open(resultFileN, "w");
    dictUrls = {}

    #load and initialize id-to-url map
    with open(nodesDict, 'r') as nodeFile:
        for line in nodeFile:
            vars = line.split(',');
            id = int(vars[0]);
            url = vars[1].strip('\n');
            dictUrls[id] = url;

    for id in iter(nodes):
        resultFile.write(str(id) + "," + dictUrls[id] + "\n");
    resultFile.close();               

def main():
    global year;
    global dirPath;
    global resultFileN;
    global nodesDict;
    global threads;    

    print "Starting Main Thread"

    if (not len(sys.argv) > 4):
        print ("Usage: get-uniq-nodes-t.py <year-month> <path-to-ukD edges file> <nodesDictionary> <outDir>");
        exit();
    
    year = sys.argv[1];
    dirPath = sys.argv[2];
    nodesDict = sys.argv[3];
    resultFileN = sys.argv[4] + resultDir + year;

    print "Beginning program to parse file and create node listings for nodes, ids and months of occurence\n"

    #Create new threads
    for numThreads in range (1, 13):
        threads.append(ParseThread(numThreads, "Thread-" + str(numThreads)))
    
    try:
        for t in threads:
            t.start()

        for t in threads:
            t.join()
    except Exception:
        print traceback.format_exc()
        sys.exit(1)

    writeRecords()
    print "Exiting Main Thread"

if __name__ == "__main__":
    main()
