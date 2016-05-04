import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all publication authors listed in dblp.xml and assigns each author a unique id number\n";

#example output: format 'node-id,node-attribute,year1,year2,year3... year?'

idNo = 1;
dictAuthors = collections.OrderedDict();
fileRef = {};
resultFiles = [];
min_year = 1936;
max_year = 2016;
resultFileName = "./results/Nodes-set1.txt";
prefix = './results/set2/nodes/nodes';
suffix = '-01-01.txt';

def parse(parseFileName):
    global dictAuthors;
    global resultFiles;
    global fileRef;

    try:
            os.remove(resultFileName);
    except OSError:
            pass;

    for year in range(min_year, max_year + 1):
        yearFile = prefix + str(year) + suffix;
        #print "yearfile-->", yearFile
        resultFiles.append(yearFile);

        try:
            os.remove(yearFile);
        except OSError:
            pass;

        ref = open(yearFile, 'a');
        fileRef.update({yearFile : ref});

    tree = ET.parse(parseFileName);	
    root = tree.getroot();

    for child in root:
        allAuthors = child.findall('author');
        pubYear = child.find('year');

        processRecord(allAuthors, pubYear);

    writeIds();

    for name, file in fileRef.items():
        file.close();
	
def processRecord(authors, yr):
    global dictAuthors;
    global idNo;

    for auth in authors:
        if not ((auth is None) or (yr is None)):
            author =  auth.text;
            year = int(yr.text);

            if not author in dictAuthors: # check if author record already exists
                dictAuthors.update({author : idNo});
                idNo += 1;

            rFile = prefix + str(year) + suffix;
            ref = fileRef[rFile];
            print "writing for year-->", year
            output = str(dictAuthors[author]) + "," + author;
            ref.write(output.encode('utf-8') + "\n");
           
                
def writeIds():
    resultFile = open(resultFileName, 'a');

    for a, id in dictAuthors.iteritems():
        output = str(id) + "," + a;
        resultFile.write(output.encode('utf-8') + '\n');
	
    resultFile.close();

def main():
    if (not len(sys.argv) > 1):
        print ("Error: you must provide a dblp xml file to parse from");
        exit();
    
    arg1 = sys.argv[1];
    parse(arg1);


if __name__ == "__main__":
    main()
