import sys;
import os;
import glob;
import collections;

#author: Halima Olapade
#date: April 2015
#example output: format 'edge1 edge2 year numOccur'

dictWords = {};
dictOccur = {};
dictEdges = collections.OrderedDict(); #stores all authors alongside publication dates
resultFileN = "/results/set1/Edges-set1-attr.txt";
minYear = 2015;
maxYear = 1700;

def parse(resultsPath, dirPath, nodesFileN):
    global dictAuthors;
    global dictEdges;    
    global dictOccur;
    global resultFileN;

    print "Beginning program to parse file and create edge listings for set1 with edge attributes\n"
    
    resultFileN = resultsPath + resultFileN
    #load word-to-id map
    with open(nodesFileN, 'r') as edgeFile:
        for line in edgeFile:
            vars = line.split(',');
            id = vars[0];
            word = vars[1].strip('\n');
            dictWords[word] =  id;

    try:
        os.remove(resultFileN);
    except OSError:
        pass;

    #open result file to write
    resultFile = open(resultFileN, 'w');

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

                #error checking: ensure both keys exist
                if not ((firstW in dictWords) and (secW in dictWords)):
                    continue;
   
                #create edge key = edge1 edge2 
                edgeKey = dictWords[firstW] + " " + dictWords[secW];
                
                for k in range(3, listSize):
                    tok = args[k].split(",")
                    year = int(tok[0])
                    occurNum = int(tok[1])    
                    occurKey = edgeKey + " " + str(year)

                    if not edgeKey in dictEdges: # check if edge record already exists
                        dictEdges.update({edgeKey : [year]});
                    else:
                        if not year in dictEdges[edgeKey]: # prevent duplicate edge occurence years
                            dictEdges[edgeKey].append(year); #append year to occurrence list
                    dictOccur.update({occurKey : occurNum})

            writeRecords(resultFile);
            dictOccur.clear();
            dictEdges.clear();     
    resultFile.close();

    print "Min Year: ", minYear
    print "Max Year: ", maxYear    
            
def writeRecords(rfile):
    global minYear;
    global maxYear;

    for a, years in dictEdges.iteritems():
        years.sort();

        for y in years:
            output = a + " " + str(y); 
            numOccur = dictOccur[output]      
            rfile.write(output + ' ' + str(numOccur) + '\n');
            
            if (y < minYear):
                minYear = y
            elif (y > maxYear):
                maxYear = y

def main():
    if (not len(sys.argv) > 3):
        print ("Error: you must provide path to results dir, edges listing in set1 notation, and file containing node id mapping");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        arg3 = sys.argv[3];
        parse(arg1, arg2, arg3);

if __name__ == "__main__":
    main()
