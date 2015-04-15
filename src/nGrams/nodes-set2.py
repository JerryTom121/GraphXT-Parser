import sys;
import os;
import collections;

#author: Halima Olapade
#date: April 2015
#example output: format '1,word'

dictYears = {};
dictWords = collections.OrderedDict();
resultFiles = [];
prefix = './results/set2/nodes/nodes';
suffix = '.txt';

def parse(nodesFileN, yearsFileN):
    global dictWords;
    global dictYears;
    global resultFiles;

    print "Beginning program to parse file and create edge listings for set2\n"

    #load years between data interval e.g 1520 - 2008
    with open(yearsFileN, 'r') as yearsFile:
        for line in yearsFile:
            output = prefix + str(line.strip("\n")) + suffix;
            resultFiles.append(output);

    #load word-to-id map
    with open(nodesFileN, 'r') as nodeFile:
        for line in nodeFile:
            args = line.split(",");
            idNum = args[0];
            word = args[1].strip('\n');
            firstYear = args[2].strip('\n');
            listSize = len(args)

            dictWords.update({word : idNum});
            dictYears.update({word : [firstYear]});
            
            for k in range(3, listSize): 
                dictYears[word].append(args[k].strip('\n'))                       

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

    for a,y in dictYears.items():
        for year in y:
            resultFile = prefix + year + suffix;
            ref = fileRef[resultFile];
            output = dictWords[a] + " " + a;
            ref.write(output + "\n");
     
    for name, file in fileRef.items():
        file.close();
                
def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide a nodes dictionary file and file containing all years to map");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        parse(arg1, arg2);


if __name__ == "__main__":
    main()
