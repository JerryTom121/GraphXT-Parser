import sys;
import os;
import collections;
import xml.etree.ElementTree as ET

#author: Halima Olapade
#date: Feb 2015

print "This is an xml parser script that parses the DBLP xml provided at http://www.informatik.uni-trier.de/~ley/db/\n";
print "The program generates a list of all publication authors listed in dblp.xml and assigns each author a unique identification number\n";
print "The output of the program are stored in the results/set2/nodes directory, there should be 80 files .txt outputted to the directory\n";

#example output: format (one file per year) 'node-id,node-attribute'

dictYears = {};
dictAuthorUrls = {};
dictAuthors = collections.OrderedDict();
resultFiles = [];
prefix = './results/set2/nodes/nodes';
suffix = '-01-01.txt';

def parse(parseFileName, yearsFileName):
    global dictAuthors;
    global dictYears;
    global resultFiles;
    global prefix;
    global suffix;

    tree = ET.parse(parseFileName);
    root = tree.getroot();

    print "[info] processing author url records..."
    for child in root:
        title = child.find('title');

        if title.text == "Home Page":
            author = child.findall('author');
            url = child.find('url');

            if url is not None:
                processUrlRecord(author, url.text);

    with open(yearsFileName, 'r') as yearsFile:
        min_year = int(yearsFile.readline().strip("\n"))
        max_year = int(yearsFile.readline().strip("\n"))

    for year in range(min_year, max_year + 1):
        output = prefix + str(year) + suffix;
        resultFiles.append(output);

    with open(parseFileName, 'r') as parseFile:
        for line in parseFile:
            args = line.strip("\n").split("|");
            id_num = args[0];
            author = args[1];
            years = args[2].split(",");

            dictAuthors.update({author : id_num});
            dictYears.update({author : years});

    processRecord();

def processUrlRecord(author, url):
    global dictAuthorUrls;

    for auth in author:
        if not (auth is None):
            author = auth.text;

            if not author in dictAuthorUrls:  # check if author record already exists
                dictAuthorUrls.update({author: url});

def processRecord():
    global dictAuthors;
    global dictYears;
    global prefix;
    global suffix;

    fileRef = {};
    write_template = "{},{},{}\n"

    # open all result files
    for yearFile in resultFiles:
        try:
            os.remove(yearFile);
        except OSError:
            pass;

        ref = open(yearFile, 'a');
        fileRef.update({yearFile : ref});

    # for a,b in fileRef.items():
    #    print a,b;

    for a,y in dictYears.items():
        url = ""
        if a in dictAuthorUrls:
            url = dictAuthorUrls[a];

        for year in y:
            resultFile = prefix + year + suffix;
            ref = fileRef[resultFile];
            output = write_template.format(dictAuthors[a], a, url);
            ref.write(output + "\n");

    for name, file in fileRef.items():
        file.close();

def main():
    if (not len(sys.argv) > 2):
        print ("Error: you must provide an xml file to parse from and file containing node id mapping");
        exit();

    arg1 = sys.argv[1];
    arg2 = sys.argv[2];
    parse(arg1, arg2);


if __name__ == "__main__":
    main()
