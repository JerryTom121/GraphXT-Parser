import sys;
import os;
import glob;
import collections;

#author: Halima Olapade
#date: April 2015

dictWords = collections.OrderedDict();
dictYears = collections.OrderedDict();
resultFileN = './results/allNodes.txt';

def parse(dirPath):
    global resultFile;    
    idNo = 1   

    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(dirPath, '*.*')):
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
            
                if not firstW in dictWords:
                    dictWords.update({firstW : idNo});
                    idNo += 1
                
                if not secW in dictWords:
                    dictWords.update({secW : idNo});
                    idNo += 1

                #add year information for edge occurrence
                for k in range(3, listSize):
                    tok = args[k].split(",")
                    year = int(tok[0])
                    occur = int(tok[1])
                
                    #check for first word
                    if not firstW in dictYears:
                        dictYears.update({firstW : [year]})
                    else:
                        if not year in dictYears[firstW]:
                            dictYears[firstW].append(year);
                    
                    #check for second word
                    if not secW in dictYears:
                        dictYears.update({secW : [year]})
                    else:
                        if not year in dictYears[secW]:
                            dictYears[secW].append(year);                            

    writeRecords();                

def writeRecords():
    resultFile = open(resultFileN, "w");

    for w, id in dictWords.iteritems():
        idNum = dictWords[w];
        output = str(idNum) + "," + w + "," + ','.join(map(str, dictYears[w]));
        resultFile.write(output + "\n");
    resultFile.close();               

def main():
    if (not len(sys.argv) > 1):
        print ("Error: you must provide a directory containing txt files to read from");
        exit();
    else:
        arg1 = sys.argv[1];
        parse(arg1);


if __name__ == "__main__":
    main()
