import sys;
import os;
import glob;
import collections;

#author: Halima Olapade
#date: April 2015

#example output: format 'edge1 edge2 year'

dictWords = {};
dictEdges = collections.OrderedDict(); #stores all authors alongside publication dates
resultFileN = "./results/set1/Edges-set1.txt";

def parse(dirPath, nodesFileN):
    global dictAuthors;
    global dictEdges;    

    print "Beginning program to parse file and create edge listings for set1\n"

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

                #error checking: ensure both keys exist
                if not ((firstW in dictWords) and (secW in dictWords)):
                    continue;
   
                #create edge key = edge1 edge2 
                edgeKey = dictWords[firstW] + " " + dictWords[secW];
                
                for k in range(3, listSize):
                    tok = args[k].split(",")
                    year = int(tok[0])
                    occur = int(tok[1])    

                    if not edgeKey in dictEdges: # check if edge record already exists
                        dictEdges.update({edgeKey : [year]});
                    else:
                        if not year in dictEdges[edgeKey]: # prevent duplicate edge occurence years
                            dictEdges[edgeKey].append(year); #append year to occurrence list

    writeRecords();     
                
def writeRecords():
    resultFile = open(resultFileN, 'w');	
    minYear = 2015;
    maxYear = 1700;	

    for a, years in dictEdges.iteritems():
        years.sort();

        for y in years:
            output = a + " " + str(y);       
            resultFile.write(output + '\n');
            
            if (y < minYear):
                minYear = y
            elif (y > maxYear):
                maxYear = y
	
    resultFile.close();	

    print "Min Year: ", minYear
    print "Max Year: ", maxYear

def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide an xml file to parse from and file containing node id mapping");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        parse(arg1, arg2);

if __name__ == "__main__":
    main()
