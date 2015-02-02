import sys;
import os;
import xml.etree.ElementTree as ET

print "\nThis is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/";
print "The program generates a list of all co-author relationships between authors list in the document\n";

def parse(parseFileName):
	global dictEdges;
	resultFileName = "DBLPEdges.txt";
	
	dictEdges = {} #stores all authors alongside publication dates

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
				#print ("on Author: ", i, " on CoAuthor: ", num);
				coAuthor = authors[num].text;				

				if(auth > coAuthor): #auth comes behind alphabetically
					firstAuth = coAuthor;
					secondAuth = auth;
				else:
					firstAuth = auth;
					secondAuth = coAuthor;

				authKey = firstAuth + "|" + secondAuth;
				#print ("Authkey: ", authKey);	
		
				if not authKey in dictEdges: # check if edge record already exists
					dictEdges.update({authKey : [year]});
				else:
					if not year in dictEdges[authKey]: # prevent duplicate publication years
						dictEdges[authKey].append(year); #append year to publication list
		index = index + 1;
                
def writeRecords(file):
	resultFile = open(file, 'a');	
	
	for a, y in dictEdges.iteritems():
		y.sort();
		output = a + "|" + ','.join(map(str, y)) ;		
		resultFile.write(output.encode('utf-8') + '\n');

		#print a, y;
	
	#print('\n');
	
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
