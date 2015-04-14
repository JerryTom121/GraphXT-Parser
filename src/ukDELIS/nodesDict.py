import sys;
import os;
import collections;

#author: Halima Olapade
#date: April 2015

print "This program assigns unique integer ids to every line in a text file and puts the results in the \'./results/nodesDict.txt\' file"

resultFileName = './results/nodesDict.txt';

def parse(parseFileName):
    lineIndex = 1

    try:
        os.remove(resultFileName);
    except OSError:
        pass;

    resultFile = open(resultsFileName, "w");

    with open(parseFileName, 'r') as parseFile:
        for line in parseFile:
            output = lineIndex + str(line.strip("\n"));
            resultFile.write(output)
            lineIndex += 1;

    with open(parseFileName, 'r') as parseFile:
        for line in parseFile:
            args = line.strip("\n").split("|");
            idNum = args[0];
            author = args[1];
            years = args[2].split(",");

            dictAuthors.update({author : idNum});
            dictYears.update({author : years});

def main():
    if (not len(sys.argv) > 1):
        exit();
    else:
        arg1 = sys.argv[1];
        parse(arg1);


if __name__ == "__main__":
    main()
