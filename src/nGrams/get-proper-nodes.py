import sys;
import os; 
import re;
import collections;

#author: Halima Olapade
#date: April 2015

print "This program assigns unique integer ids to every line in a text file and puts the results in the \'results/propeNodesDict.txt\' file of the results path passed in"

resultFileN = 'results/properNodesDict.txt';

def parse(resultsPath, parseFileName):
    global resultFileN;

    lineIndex = 1 
    resultFileN = resultsPath + resultFileN;
    
    try:
        os.remove(resultFileN);
    except OSError:
        pass;

    resultFile = open(resultFileN, "w");

    with open(parseFileName, 'r') as parseFile:
        for l in parseFile:
            args = l.split(",")
            line = args[1].strip('\n')

            #if (bool(re.search(r'\d', line)) == True):
            #    continue;
            if (line == ''):
                continue;
    
            output = str(lineIndex) + "," + line + "\n"
            resultFile.write(output)
            lineIndex += 1;

def main():
    if (not len(sys.argv) > 2): 
        exit();
    
    arg1 = sys.argv[1];
    arg2 = sys.argv[2];
    parse(arg1, arg2);

if __name__ == "__main__":
    main()
