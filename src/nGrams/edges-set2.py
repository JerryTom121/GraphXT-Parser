import sys;
import os;
import glob;
import collections;

#author: Halima Olapade
#date: April 2015

#example output: format '1 2'

dictYears = {};
resultFiles = [];
fileRef = {}; 
prefix = '/results/set2/edges/edges';
suffix = '.txt';

def parse(resultsPath, edgesDirPath, yearsFileN):
    global dictYears;
    global resultFiles;
    global fileRef;
    global prefix;

    print "Beginning program to parse file and create edges listings for set2\n"

    prefix = resultsPath + prefix

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

    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(edgesDirPath, '*')):
        with open(fileN, "r") as edgesFile:
            print("Current file: " + edgesFile.name)

            for line in edgesFile:
                args = line.split(" ");
                id1 = args[0].strip("\n");
                id2 = args[1].strip("\n");
                year = args[2].strip("\n");
                edgeKey = str(id1) + " " + str(id2);
           
                if not edgeKey in dictYears:
                    dictYears.update({edgeKey : [year]});
                else:
                    dictYears[edgeKey].append(year);
            
            processRecord();            
            dictYears.clear();

    #close all results files
    for name, file in fileRef.items():
        file.close();

def processRecord():
    for edgeKey,y in dictYears.items():
        for year in y:
            resultFile = prefix + year + suffix;
            ref = fileRef[resultFile];
            ref.write(edgeKey + "\n");
     
def main():
    if (not len(sys.argv) > 3):
        print ("Error: you must provide path to results dir, an edges dictionary file to parse from and file containing all years to map");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        arg3 = sys.argv[3];
        parse(arg1, arg2, arg3);


if __name__ == "__main__":
    main()
