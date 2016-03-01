import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2016

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all co-author relationships between authors listed in t    he document as well as the year of the joint publication in 'AuthorID1|AuthorID2 format\n";

#example output: format 'id1 id2 title record_type'

dictAuthors = {};
dictEdges = collections.OrderedDict(); #stores all authors alongside publication dates
edgesFiles = [];
prefix = './results/edges/edges';
suffix = '-01-01.txt';
minYear = 2050;
maxYear = -1;

def parse(parseFileName, nodesFileName):
    global dictAuthors;
    global dictEdges;
    global edgesFiles;
    
    #load author name-to-id map
    with open(nodesFileName, 'r') as nodeFile:
        for line in nodeFile:
            args = line.split(',');
            authid = args[0];
            authName = args[1].strip('\n');
            dictAuthors[authName] = authid;

    tree = ET.parse(parseFileName); 
    root = tree.getroot();

    print "[info] edges.py: processing author records..."
    for child in root:
        tl = child.find('title')
        record_type = child.tag.replace(" ", "_")
        title = tl.text.replace(" ", "_").replace(".", "")
        pubYear = child.find('year')
        allAuthors = child.findall('author')

        if record_type == "www":
            record_type = "article"
    
        processRecords(allAuthors, pubYear, title, record_type);

    for year in range(minYear, maxYear + 1):
        output = prefix + str(year) + suffix;
        edgesFiles.append(output);

    print "[info] edges.py: writing records..."
    writeRecords();

    print "[info] edges.py: done."

def processRecords(authors, yr, title, record_type):
    global dictEdges;
    global minYear;
    global maxYear;
    auth_key_template = "{} {} {} {}"

    if len(authors) < 2: #error checking, return if only one author for a publication
        return;

    index = 1;
    numAuthors = len(authors);
    
    for a in authors:
        if not ((a is None) or (yr is None)):
            auth = a.text;
            year = int(yr.text);
            firstAuth = "";
            secondAuth = "";

            if(year < minYear):
                minYear = year
            elif(year > maxYear):
                maxYear = year

            for num in range(index, numAuthors): #iterate through all co authors
                coAuthor = authors[num].text;               

                if(auth > coAuthor): #auth comes behind alphabetically
                    firstAuth = coAuthor.encode('utf-8');
                    secondAuth = auth.encode('utf-8');
                else:
                    firstAuth = auth.encode('utf-8');
                    secondAuth = coAuthor.encode('utf-8');
                
                #authKey = dictAuthors[firstAuth] + " " + dictAuthors[secondAuth];
                authKey = auth_key_template.format(dictAuthors[firstAuth], dictAuthors[secondAuth], title, record_type)
        
                if not authKey in dictEdges: # check if edge record already exists
                    dictEdges.update({authKey : [year]});
                else:
                    if not year in dictEdges[authKey]: # prevent duplicate publication years
                        dictEdges[authKey].append(year); #append year to publication list
        index = index + 1;

def writeRecords():
    fileRef = {};

    #open all edges files
    for yearFile in edgesFiles:
        try:
            os.remove(yearFile);
        except OSError:
            pass;

        ref = open(yearFile, 'a');
        fileRef.update({yearFile : ref}); 

    for authKey,y in dictEdges.items():
        for year in y:
            resultFile = prefix + str(year) + suffix;
            ref = fileRef[resultFile];
            ref.write(authKey + "\n");
     
    for name, file in fileRef.items():
        file.close();
                
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
