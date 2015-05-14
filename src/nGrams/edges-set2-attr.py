import sys;
import os;
import glob;
import collections;

#author: Halima Olapade
#date: April 2015

#example output: format 'edge1 edge2 numOccur'

dictWords = {};
dictEdges = {};
dictOccur = {};
resultFiles = [];
fileRef = {}; 
prefix = '/results/set2/edges/edges';
suffix = '.txt';

def parse(resultsPath, edgesDirPath, nodesFileN, yearsFileN):
    global dictEdges;
    global dictWords;
    global dictOccur;
    global resultFiles;
    global fileRef;
    global prefix;

    print "Beginning program to parse file and create edges listings for set2 with edge attributes\n"

    prefix = resultsPath + prefix
    print "Prefix: ", prefix

    with open(yearsFileN, 'r') as yearsFile:
        for line in yearsFile:
            output = prefix + str(line.strip("\n")) + suffix;
            resultFiles.append(output);
    
    #open all results files
    for yearFile in resultFiles:
        try:
            os.remove(yearFile);
        except OSError:
            pass;

        ref = open(yearFile, 'a');
        fileRef.update({yearFile : ref}); 

    #load word-to-id map
    with open(nodesFileN, 'r') as edgeFile:
        for line in edgeFile:
            vars = line.split(',');
            id = vars[0];
            word = vars[1].strip('\n');
            dictWords[word] =  id; 

    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(edgesDirPath, '*')):
        with open(fileN, "r") as edgesFile:
            print("Current file: " + edgesFile.name)

            firstW = ""
            secW = ""

            for line in edgesFile:
                args = line.split("\t");
                edgeWords = args[1].split(" ");
                listSize = len(args)

                #if phrase contains 3 words, take the first and last
                if(len(edgeWords) > 2): 
                    firstW = (edgeWords[0].split("/"))[0] 
                    secW = (edgeWords[-1].split("/"))[0]
                else:
                    firstW = (edgeWords[0].split("/"))[0]
                    secW = (edgeWords[1].split("/"))[0]

                #error checking: ensure both keys exist
                if not ((firstW in dictWords) and (secW in dictWords)):
                    continue;
   
                #create edge key = edge1 edge2 
                edgeKey = dictWords[firstW] + " " + dictWords[secW];
    
                for k in range(3, listSize):
                    tok = args[k].split(",")
                    year = int(tok[0])
                    occurNum = int(tok[1])    
                    occurKey = edgeKey + " " + str(year)

                    if not edgeKey in dictEdges: # check if edge record already exists
                        dictEdges.update({edgeKey : [year]});
                    else:
                        if not year in dictEdges[edgeKey]: # prevent duplicate edge occurence years
                            dictEdges[edgeKey].append(year); #append year to occurrence list
                    dictOccur.update({occurKey : occurNum})

            processRecords();
            dictOccur.clear();
            dictEdges.clear(); 

    #close all results files
    for name, file in fileRef.items():
        file.close();

def processRecords():
    for edgeKey,y in dictEdges.items():
        for year in y:
            resultFile = prefix + str(year) + suffix;
            ref = fileRef[resultFile];
            occurKey = dictOccur[edgeKey + " " + str(year)]
            ref.write(edgeKey + " " + str(occurKey) + "\n");
     
def main():
    if (not len(sys.argv) > 4):
        print ("Error: you must provide path to the results dir, path to the raw edges listing, all nodes dictionary and a file containing all years to map");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        arg3 = sys.argv[3];
        arg4 = sys.argv[4];
        parse(arg1, arg2, arg3, arg4);


if __name__ == "__main__":
    main()
