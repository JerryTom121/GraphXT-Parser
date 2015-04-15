import sys;
import os;
import collections;

#author: Halima Olapade
#date: April 2015

#example output: format '1 2'

dictYears = {};
resultFiles = [];
prefix = './results/set2/edges/edges';
suffix = '.txt';

def parse(edgesFileN, yearsFileN):
    global dictEdges;
    global dictYears;
    global resultFiles;

    print "Beginning program to parse file and create nodes listings for set2\n"

    with open(yearsFileN, 'r') as yearsFile:
        for line in yearsFile:
            output = prefix + str(line.strip("\n")) + suffix;
            resultFiles.append(output);

    with open(edgesFileN, 'r') as edgesFile:
        for line in edgesFile:
            args = line.split(" ");
            id1 = args[0];
            id2 = args[1];
            year = args[2];
            edgeKey = str(id1) + " " + str(id2);
           
            if not edgeKey in dictYears:
                dictYears.update({edgeKey : [year]});
            else:
                if not year in dictEdges[edgeKey]:
                    dictYears[edgeKey].append(year);

    processRecord();
	

def processRecord():
    fileRef = {};

    #open all result files
    for yearFile in resultFiles:
        try:
            os.remove(yearFile);
        except OSError:
            pass;

        ref = open(yearFile, 'a');
        fileRef.update({yearFile : ref}); 

    for edgeKey,y in dictYears.items():
        for year in y:
            resultFile = prefix + year + suffix;
            ref = fileRef[resultFile];
            ref.write(edgeKey + "\n");
     
    for name, file in fileRef.items():
        file.close();
                
def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide an edges dictionary file to parse from and file containing all years to map");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        parse(arg1, arg2);


if __name__ == "__main__":
    main()
