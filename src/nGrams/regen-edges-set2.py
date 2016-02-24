import sys;
import glob;
import os;
import collections;

#author: Halima Olapade
#date: April 2015
#example output: format '1,word'

newIdsDict = {};
oldIdsDict = {};

def parse(resultsPath, oldNodesN,  newNodesN, oldEdgesDir):
    global newIdsDict;
    global oldIdsDict;

    print "Beginning program to parse file and create edge listings for set2\n"

    with open(newNodesN, 'r') as nodeFile:
        for line in nodeFile:
            args = line.split(",");
            idNum = args[0];
            word = args[1].strip('\n');

            newIdsDict.update({word : idNum});

    with open(oldNodesN, 'r') as nodeFile:
        for line in nodeFile:
            args = line.split(",");
            idNum = int(args[0]);
            word = args[1].strip('\n');

            oldIdsDict.update({idNum : word});

    print "OldEdgesDir: ", oldEdgesDir

    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(oldEdgesDir, '*')):
        with open(fileN, "r") as oldEdgesFile:
            print("Current file: " + oldEdgesFile.name)
                      
            filename = oldEdgesFile.name.split("/")[-1]
            resultFileN = resultsPath + "/" + filename

            if not os.path.isfile(resultFileN):
                res = open(resultFileN, "w")           
    
                for line in oldEdgesFile:
                    args = line.split(" ")
                    id1 = int(args[0])
                    id2 = int(args[1])
                    occur = args[2]

                    word1 = oldIdsDict[id1]
                    word2 = oldIdsDict[id2]

                    if word1 == '' or word2 == '':
                        continue;

                    if ((word1 in newIdsDict) and (word2 in newIdsDict)):
                        output = newIdsDict[word1] + " " + newIdsDict[word2] + " " + occur
                        res.write(output)

                res.close()
                
def main():
    if (not len(sys.argv) > 4):
        print ("Error: you must provide the path to dir containing results, a nodes dictionary file and file containing all years to map");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        arg3 = sys.argv[3];
        arg4 = sys.argv[4];
        parse(arg1, arg2, arg3, arg4);


if __name__ == "__main__":
    main()
