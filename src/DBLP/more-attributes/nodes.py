import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2016

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";

#example output: format 'node-id,author,author-url'

idNo = 1;
dictAuthors = collections.OrderedDict();
dictYears = {};
dictAuthorUrls = {};
nodesFiles = [];
nodesDictName = './results/NodesDict.txt';
prefix = './results/nodes/nodes';
suffix = '-01-01.txt';
minYear = 2050;
maxYear = -1;


def parse(parseFileName):
    global dictAuthors;

    tree = ET.parse(parseFileName);	
    root = tree.getroot();

    print "[info] processing author records..."
    for child in root:
        allAuthors = child.findall('author');
        pubYear = child.find('year');

        processAuthorRecord(allAuthors, pubYear);

    print "[info] processing author url records..."
    for child in root:
        title = child.find('title');

        if title.text == "Home Page":
            author = child.findall('author');
            url = child.find('url');

            if url is not None:
                processUrlRecord(author, url.text);

    for year in range(minYear, maxYear + 1):
        output = prefix + str(year) + suffix;
        nodesFiles.append(output);

    print "[info] writing records..."
    writeRecords();

    print "[info] done."
	
def processUrlRecord(author, url):
    global dictAuthorUrls;

    for auth in author:
        if not (auth is None):
            author = auth.text;
    
            if not author in dictAuthorUrls: # check if author record already exists
                dictAuthorUrls.update({author : url});

def processAuthorRecord(authors, yr):
    global dictAuthors;
    global dictYears;
    global idNo;
    global minYear;
    global maxYear;

    for auth in authors:
        if not ((auth is None) or (yr is None)):
            author =  auth.text;
            year = int(yr.text);

            if(year < minYear):
                minYear = year
            elif(year > maxYear):
                maxYear = year
    
            if not author in dictAuthors: # check if author record already exists
                dictAuthors.update({author : idNo});
                dictYears.update({author : [year]});
                idNo += 1;
                #print author, "-->", year
            else:
                if not year in dictYears[author]:
                    dictYears[author].append(year);

def writeRecords():
    fileRef = {};
    write_template = "{},{},{}\n"
    nodes_write_template = "{},{}\n"

    #open all nodes files
    for yearFile in nodesFiles:
        try:
            os.remove(yearFile);
        except OSError:
            pass;

        ref = open(yearFile, 'a');
        fileRef.update({yearFile : ref}); 

    nodesDictFile = open(nodesDictName, 'w');

    for a,y in dictYears.items():
        idNum = dictAuthors[a];
        nodesOutput = nodes_write_template.format(str(idNum), a.encode('utf-8'))
        nodesDictFile.write(nodesOutput)

        for year in y:
            resultFile = prefix + str(year) + suffix;
            ref = fileRef[resultFile];
            authorid = str(dictAuthors[a])
            url = ""

            if a in dictAuthorUrls:
                url = dictAuthorUrls[a]

            output = write_template.format(authorid, a.encode('utf-8'), url)
            ref.write(output);
    
    nodesDictFile.close() 
    for name, file in fileRef.items():
        file.close();

def main():
    if (not len(sys.argv) > 1):
        print ("Error: you must provide a dblp xml file to parse from");
        exit();
    
    arg1 = sys.argv[1];
    parse(arg1);

def trace(frame, event, arg):
    if frame.f_code.co_filename == "nodes.py":
        print "%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno)
    return trace

sys.settrace(trace)

if __name__ == "__main__":
    main()
