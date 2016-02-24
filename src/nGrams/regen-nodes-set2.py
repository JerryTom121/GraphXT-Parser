import sys;
import glob;
import os;
import collections;

#author: Halima Olapade
#date: April 2015
#example output: format '1,word'

newIdsDict = {};

def parse(resultsPath, newNodesN, oldNodesDir):
    global newIdsDict;
    global prefix;

    print "Beginning program to parse file and create edge listings for set2\n"

    #load word-to-id map
    with open(newNodesN, 'r') as nodeFile:
        for line in nodeFile:
            args = line.split(",");
            idNum = args[0];
            word = args[1].strip('\n');

            newIdsDict.update({word : idNum});

    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(oldNodesDir, '*')):
        with open(fileN, "r") as oldNodesFile:
            print("Current file: " + oldNodesFile.name)
           
            filename = oldNodesFile.name.split("/")[-1]
            resultFileN = resultsPath + "/" + filename
            res = open(resultFileN, "w")
             
            for line in oldNodesFile:
                args = line.split(",")
                word = args[1].strip('\n')

                if word in newIdsDict:
                    output = newIdsDict[word] + "," + word + "\n"
                    res.write(output)

            res.close()

                
def main():
    if (not len(sys.argv) > 3):
        print ("Error: you must provide the path to dir containing results, a nodes dictionary file and file containing all years to map");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        arg3 = sys.argv[3];
        parse(arg1, arg2, arg3);


if __name__ == "__main__":
    main()
