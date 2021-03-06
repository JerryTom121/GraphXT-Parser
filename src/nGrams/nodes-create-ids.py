import sys;
import os;
import glob;
import collections;

#author: Halima Olapade
#date: April 2015

dictWords = collections.OrderedDict();
dictYears = collections.OrderedDict();
resultFileN = '/results/nodesDict.txt';

def parse(resultsPath, dirPath):
    global resultFile; 
    global resultFileN;   
    idNo = 1   

    resultFileN = resultsPath + resultFileN

    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(dirPath, '*')):
        with open(fileN, "r") as file:
            print("Current file: " + file.name)
        
            firstW = ""
            secW = ""
            for line in file:
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
           
                #skip words that contain a comma
                if (firstW.find(",") != -1) or (secW.find(",") != -1):
                    continue;
 
                if not firstW in dictWords:
                    dictWords.update({firstW : idNo});
                    idNo += 1
                
                if not secW in dictWords:
                    dictWords.update({secW : idNo});
                    idNo += 1

    writeRecords();                

def writeRecords():
    resultFile = open(resultFileN, "w");

    for w, id in dictWords.iteritems():
        idNum = dictWords[w];
        output = str(idNum) + "," + w + "," + ','.join(map(str, dictYears[w]));
        resultFile.write(output + "\n");
    resultFile.close();               

def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide a path to the result dir, a directory containing txt files to read from");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        parse(arg1, arg2);


if __name__ == "__main__":
    main()
