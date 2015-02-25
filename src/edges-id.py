import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "\nThis is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/";
print "The program generates a list of all co-author relationships between authors listed in the document as well as the year of the joint publication in 'AuthorID1|AuthorID2|Year' format \n";

#example output: format 'AuthorID1|AuthorID2|Year'

dictAuthors = {}
dictEdges = collections.OrderedDict() #stores all authors alongside publication dates

def parse(parseFileName, edgesFileName):
    global dictAuthors;

    resultFileName = "../results/Edges-ID.txt";
    
    #load author name-to-id map
    with open(edgesFileName, 'r') as edgeFile:
        for line in edgeFile:
            vars = line.split('|');
            id = vars[0];
            authName = vars[1].strip('\n');
            dictAuthors[authName] =  id;

    try:
        os.remove(resultFileName);
    except OSError:
        pass;

    tree = ET.parse(parseFileName);	
    root = tree.getroot();

    for child in root:
        allAuthors = child.findall('author');
        pubYear = child.find('year');
	
        processRecords(allAuthors, pubYear);

    writeRecords(resultFileName);
	
def processRecords(authors, yr):
    global dictEdges;

    if len(authors) < 2: #error checking, return if only one author for a publication
        return;

    index = 1;
    numAuthors = len(authors);
	
    for a in authors:
        if not ((a is None) or (yr is None)):
            auth = a.text;
            year = yr.text;	
            firstAuth = "";
            secondAuth = "";

            for num in range(index, numAuthors): #iterate through all co authors
                coAuthor = authors[num].text;				

                if(auth > coAuthor): #auth comes behind alphabetically
                    firstAuth = coAuthor.encode('utf-8');
                    secondAuth = auth.encode('utf-8');
                else:
                    firstAuth = auth.encode('utf-8');
                    secondAuth = coAuthor.encode('utf-8');

                authKey = dictAuthors[firstAuth] + "|" + dictAuthors[secondAuth];
		
                if not authKey in dictEdges: # check if edge record already exists
                    dictEdges.update({authKey : [year]});
                else:
                    if not year in dictEdges[authKey]: # prevent duplicate publication years
                        dictEdges[authKey].append(year); #append year to publication list
        index = index + 1;
                
def writeRecords(file):
    resultFile = open(file, 'a');	
	
    for a, years in dictEdges.iteritems():
        years.sort();

        for y in years:
            output = a + "|" + y;		
            resultFile.write(output.encode('utf-8') + '\n');
	
    resultFile.close();	

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
