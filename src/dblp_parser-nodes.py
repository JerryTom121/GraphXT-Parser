import sys;
import os;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Jan 2015

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all publication authors listed in dblp.xml along with known years of publication\n";

def parse(parseFileName):
	global dictAuthors;
	resultFileName = "DBLPNodes.txt";
	
	dictAuthors = {} #stores all authors alongside publication dates

	try:
                os.remove(resultFileName);
        except OSError:
                pass;

	tree = ET.parse(parseFileName);	
	root = tree.getroot();

	for child in root:
		allAuthors = child.findall('author');
		pubYear = child.find('year');
	
		processRecord(allAuthors, pubYear);

	writeRecords(resultFileName);
	
def processRecord(authors, yr):

	for auth in authors:
		if not ((auth is None) or (yr is None)):
			author =  auth.text;
			year = yr.text;
	
			if not author in dictAuthors: # check if author record already exists
				dictAuthors.update({author : [year]});
			else:
				if not year in dictAuthors[author]: # prevent duplicate publication years
					dictAuthors[author].append(year); #append year to publication list

                
def writeRecords(file):
	resultFile = open(file, 'a');	
	
	for a, y in dictAuthors.iteritems():
		y.sort();
		output = a + "|" + ','.join(map(str, y)) ;		
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
