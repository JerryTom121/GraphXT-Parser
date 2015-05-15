import sys;
import os;
import collections;

#author: Halima Olapade
#date: April 2015

print "This program assigns unique integer ids to every line in a text file and puts the results in the \'./results/nodesDict.txt\' file"

resultFileN = './results/nodesDict.txt';

def parse(parseFileName):
    lineIndex = 1

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
    if (not len(sys.argv) > 1):
        exit();
    else:
        arg1 = sys.argv[1];
        parse(arg1);


if __name__ == "__main__":
    main()
