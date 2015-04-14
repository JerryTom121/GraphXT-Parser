import sys;
import os;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "\nThis is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/";
print "The program generates a list of all co-author relationships between authors listed in the document as well as the year of the joint publication and publication title in 'Author1|Author2|Year|Title' format \n";

#example output: format 'Author1|Author2|Year|Title'
#Alfred Kaltenmeier|André Berton|2006|SmartKom
#André Berton|Udo Haiber|2006|SmartKom

def parse(parseFileName):
	global resultFile;
	resultFileName = "Conf-Edges.txt";
	
	try:
                os.remove(resultFileName);
        except OSError:
                pass;

	tree = ET.parse(parseFileName);	
	root = tree.getroot();

	resultFile = open(resultFileName, 'a');	
	
	for child in root:
		allAuthors = child.findall('author');
		pubYear = child.find('year');
		journal = child.find('journal');
                booktitle = child.find('booktitle');

                pubName = None;    

                if not (journal is None):
                        pubName = journal;
                elif not (booktitle is None):
                        pubName = booktitle;

                if (not (pubName is None)) and len(allAuthors) > 1: #variable was reassigned	
			processRecords(allAuthors, pubYear, pubName);

	resultFile.close();	

	
def processRecords(authors, yr, pub):
	index = 1;
	numAuthors = len(authors);
	
	for a in authors:
		if not ((a is None) or (yr is None)):
			auth = a.text;
			year = yr.text;	
			pubTitle = pub.text;
			firstAuth = "";
			secondAuth = "";

			for num in range(index, numAuthors): #iterate through all co authors
				coAuthor = authors[num].text;				

				if(auth > coAuthor): #auth comes behind alphabetically
					firstAuth = coAuthor;
					secondAuth = auth;
				else:
					firstAuth = auth;
					secondAuth = coAuthor;

				authKey = firstAuth + "|" + secondAuth;
				writeRecord(authKey, year, pubTitle);
		
		index = index + 1;

                
def writeRecord(authKey, year, pubTitle):
	output = authKey + "|" + year + "|" + pubTitle;		
	resultFile.write(output.encode('utf-8') + '\n');
	

def main():
	if (not len(sys.argv) > 1):
        	print ("Error: you must provide an xml file to parse from");
        	exit();
	else:
        	arg1 = sys.argv[1];
	parse(arg1);


if __name__ == "__main__":
    main()
