import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all publication authors listed in dblp.xml and assigns each author a unique identification number\n";
print "The output of the program are stored in the results/set2/nodes directory, there should be 80 files .txt outputted to the directory\n";

#example output: format (one file per year) 'node-id,node-attribute'

dictYears = {};
dictAuthors = collections.OrderedDict();
resultFiles = [];
prefix = './results/set2/nodes/nodes';
suffix = '.txt';

def parse(parseFileName, yearsFileName):
    global dictAuthors;
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
            idNum = args[0];
            author = args[1];
            years = args[2].split(",");

            dictAuthors.update({author : idNum});
            dictYears.update({author : years});

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

    for a,y in dictYears.items():
        for year in y:
            resultFile = prefix + year + suffix;
            ref = fileRef[resultFile];
            output = dictAuthors[a] + “,” + a;
            ref.write(output + "\n");
     
    for name, file in fileRef.items():
        file.close();
                
def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide an xml file to parse from and file containing node id mapping");
        exit();
    
    arg1 = sys.argv[1];
    arg2 = sys.argv[2];
    parse(arg1, arg2);


if __name__ == "__main__":
    main()
