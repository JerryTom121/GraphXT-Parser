import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all publication authors listed in dblp.xml and assigns each author a unique identification number\n";

#example output: format '1|Author'

idNo = 1;
dictAuthors = collections.OrderedDict();

def parse(parseFileName):
    global dictAuthors;
    resultFileName = "../results/Node-ID.txt";

    try:
            os.remove(resultFileName);
    except OSError:
            pass;

    tree = ET.parse(parseFileName);	
    root = tree.getroot();

    for child in root:
        allAuthors = child.findall('author');
        processRecord(allAuthors);

    writeRecords(resultFileName);
	
def processRecord(authors):
    global dictAuthors;
    global idNo;

    for auth in authors:
        if not (auth is None):
            author =  auth.text;
	
            if not author in dictAuthors: # check if author record already exists
                dictAuthors.update({author : idNo});
                idNo += 1;

                
def writeRecords(file):
    resultFile = open(file, 'a');	
	
    for a, id in dictAuthors.iteritems():
        output = str(id) + "|" + a ;		
        resultFile.write(output.encode('utf-8') + '\n');
	
    resultFile.close();	

def main():
    if (not len(sys.argv) > 1):
        print ("Error: you must provide an xml file to parse from");
        exit();
    else:
        arg1 = sys.argv[1];
        parse(arg1);


if __name__ == "__main__":
    main()
