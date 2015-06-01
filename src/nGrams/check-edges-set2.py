import sys;
import glob;
import os;
import re;

#author: Halima Olapade
#date: May 2015

def parse(newNodesN, nodesDir, edgesDir):
    newIdsDict = {};
    print "Beginning program to compare ids in nodes and edges files\n"

    with open(newNodesN, 'r') as nodeFile:
        for line in nodeFile:
            args = line.split(",");
            idNum = args[0];
            word = args[1].strip('\n');

            newIdsDict.update({idNum : word});

    #parse all edges files in the given directory
    for fileN in glob.glob(os.path.join(edgesDir, '*')):
        with open(fileN, "r") as edgesFile:
            print("Current file: " + edgesFile.name)
                      
            filename = edgesFile.name.split("/")[-1]
            year = re.compile('edges(.*?).txt').search(filename).group(1)
            #print "Filename:", filename, " Year:", year
            
            nodesFileN = nodesDir + '/nodes' + year + '.txt'
            print "Node File Name:", nodesFileN
            #nodesFile = open(nodesFileN, 'r')
            nodesList = {}
            
            with open(nodesFileN, "r") as nFile:
                for l in nFile:
                    args = l.split(",")
                    id = args[0]
                    nodesList.update({id : 1})

            idsToWrite = {}

            for line in edgesFile:
                args = line.split(" ")
                id1 = args[0]
                id2 = args[1]

                if id1 not in nodesList:
                    if id1 not in idsToWrite:
                        idsToWrite.update({id1 : 1})
                
                if id2 not in nodesList:
                    if id2 not in idsToWrite:
                        idsToWrite.update({id2 : 1})
            
            if len(idsToWrite) > 0:
                nodesFile = open(nodesFileN, 'a')
                
                for id in idsToWrite:
                    word = newIdsDict[id]
                    output = id + "," + word + "\n"
                    nodesFile.write(output)
                nodesFile.close()
        
            idsToWrite.clear()
            nodesList.clear()

               
def main():
    if (not len(sys.argv) > 3):
        print ("Error: not enough arguments provided");
        exit();
   
    arg1 = sys.argv[1];
    arg2 = sys.argv[2];
    arg3 = sys.argv[3];
    parse(arg1, arg2, arg3);

if __name__ == "__main__":
    main()
