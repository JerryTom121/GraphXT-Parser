import sys;
import os;
import collections;

#author: Halima Olapade
#date: April 2015

print "This program assigns unique integer ids to every line in a text file and puts the results in the \'results/nodesDict.txt\' file of the results path passed in"

resultFileN = '/results/nodesDict.txt';

def parse(resultsPath, parseFileName):
    global resultFileN;

    lineIndex = 0
    resultFileN = resultsPath + resultFileN;
    
    try:
        os.remove(resultFileN);
    except OSError:
        pass;

    resultFile = open(resultFileN, "w");

    with open(parseFileName, 'r') as parseFile:
        for line in parseFile:
            output = str(lineIndex) + "," + line
            resultFile.write(output)
            lineIndex += 1;

def main():
    if (not len(sys.argv) > 2):
        print "Error in Usage: python nodes-create-id.py /path-to-results-directory/ /path-to-ukDelis-url-listings/"
        exit();
    
    arg1 = sys.argv[1];
    arg2 = sys.argv[2];
    parse(arg1, arg2);


if __name__ == "__main__":
    main()
