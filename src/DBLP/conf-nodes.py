import sys;
import os;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all publication authors listed in dblp.xml along with known years of publication and the tile of the publication in 'Author|Year|Title' format\n";

#example output: format 'Author|Year|Title'
#Massimo Zancanaro|2012|Ubiquitous Display Environments
#Wolfgang Wahlster|2013|SemProM


def parse(parseFileName):
	global resultFile;
	resultFileName = "Conf-Nodes.txt";
	
	try:
                os.remove(resultFileName);
        except OSError:
                pass;

	tree = ET.parse(parseFileName);	
	root = tree.getroot();
	#print(root);


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

		if not (pubName is None): #variable was reassigned
			processRecord(allAuthors, pubYear, pubName);
	
	resultFile.close();	

def processRecord(authors, yr, pub):
	for auth in authors:
		if not ((auth is None) or (yr is None)):
			author =  auth.text;
			year = yr.text;
			pubTitle = pub.text;

			writeRecord(author, year, pubTitle)
               
 
def writeRecord(author, year, pubTitle):
	output = author + "|" + year + "|" + pubTitle ;		
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
