import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all co-author relationships between authors listed in t    he document as well as the year of the joint publication in 'AuthorID1|AuthorID2 format\n";
print "The output of the program are stored in the results/set2/edges directory, there should be 81 files .txt outputted to the directory\n";

#example output: format '1|2'

dictYears = {};
resultFiles = [];
prefix = '../results/set2/edges/edges';
suffix = '.txt';

def parse(parseFileName, yearsFileName):
    global dictEdges;
    global dictYears;
    global resultFiles;
    global prefix;
    global suffix;

    with open(yearsFileName, 'r') as yearsFile:
        for line in yearsFile:
            output = prefix + str(line.strip("\n")) + suffix;
            resultFiles.append(output);

    with open(parseFileName, 'r') as parseFile:
        for line in parseFile:
            args = line.strip("\n").split("|");
            id1 = args[0];
            id2 = args[1];
            years = args[2].split(",");
            authKey = str(id1) + "|" + str(id2);
           
            dictYears.update({authKey : years});

    processRecord();
	

def processRecord():
    global dictAuthors;
    global dictYears;
    global prefix;
    global suffix;

    fileRef = {};

    #open all result files
    for yearFile in resultFiles:
        try:
            os.remove(yearFile);
        except OSError:
            pass;

        ref = open(yearFile, 'a');
        fileRef.update({yearFile : ref}); 

    #for a,b in fileRef.items():
    #    print a,b;

    for authKey,y in dictYears.items():
        for year in y:
            resultFile = prefix + year + suffix;
            ref = fileRef[resultFile];
            ref.write(authKey + "\n");
     
    for name, file in fileRef.items():
        file.close();
                
def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide an xml file to parse from and file containing node id     mapping");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        parse(arg1, arg2);


if __name__ == "__main__":
    main()
