import xml.etree.ElementTree as ET
import collections
from datetime import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import sys

# stores all authors names with their unique ids
dictAuthors = collections.OrderedDict()

# lists for all nodes and edges
nodesList = []
edgesList = []

# stores all nodes and edges in dictionary to avoid duplicates
dictEdges = collections.OrderedDict()
dictNodes = {}

nodes_file_format = "{}/nodes/nodes{}.txt"
edges_file_format = "{}/edges/edges{}.txt"
year_format = "{}-01-01"
min_year = 1936
max_year = 2016

conf = SparkConf().setAppName("ParquetConverter").setMaster("local[2]")
sc = SparkContext(conf=conf)
logger = sc._jvm.org.apache.log4j
logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)
sqlContext = SQLContext(sc)


def main(root):
    counter = 1
    # reading all nodes and edges .txt files
    print ("[info] processing nodes and edges files...")

    # reading nodes files
    for yr in range(min_year, max_year):
        pub_year = year_format.format(str(yr))
        filepath = nodes_file_format.format(root, pub_year)

        print ("[info] nodes file:", filepath)
        with open(filepath, 'r') as fd:
            for line in fd:
                args = line.strip("\n").split(",")
                aid = int(args[0])
                auth = args[1]
                processAuthorNodes(aid, auth, pub_year)

    print ("\n")
    reading edges files
    for yr in range(min_year, max_year):
        pub_year = year_format.format(str(yr))
        filepath = edges_file_format.format(root, pub_year)

        print ("[info] edges file:", filepath)
        with open(filepath, 'r') as fd:
            for line in fd:
                args = line.strip("\n").split(" ")
                aid1 = int(args[0])
                aid2 = int(args[1])
                processAuthorNodes(aid1, aid2, pub_year)

    print ("[info] writing node files...")
    writeRecordsNodes()
    print ("[info] writing edges files...")
    writeRecordsEdges()
    print ("[info] done.")

def processAuthorNodes(aid, author, pub_year):
    global nodesList

    year = int(pub_year.split('-')[0]);
    dateEnd = year_format.format(str(year + 1))

    date = pub_year
    #dateEnd = datetime.strptime(yearEnd, '%Y-%m-%d') + timedelta(days=1)
    #dateEnd = dateEnd.strftime('%Y-%m-%d')
    nodesList.append([aid, author, date, dateEnd])

    #global dictAuthors;

    #if not ((author is None) or (pub_year is None)):
        #affiliation = ''
        #if len(auth) == 2:
        #    author = auth[1].text + " " + auth[0].text;
        #elif len(auth) == 3:
        #    if "affiliation" in auth[2].tag:
        #        affiliation = auth[2].text
        #        author = auth[1].text + " " + auth[0].text;
        #    else:
        #        author = auth[1].text + " " + auth[0].text + " " + auth[2].text;
        #else:
        #    author = auth[0].text;

        #auth_key_template = "{} {} {} {}"
        #year = int(pub_year.text.split('-')[0]);

        # if author does not exist in the dictionary, give id and add it
        #if author not in dictAuthors:
        #    dictAuthors.update({author: aid})
        #    authKey = auth_key_template.format(aid, author, date, dateEnd)
        #    dictNodes.update({authKey: [year]})

        # else just add it to the list
        #else:
        #    authKey = auth_key_template.format(dictAuthors[author], author, date, dateEnd)
        #    if authKey not in dictNodes:
        #        dictNodes.update({authKey: [year]})
        #        NodeList.append([dictAuthors[author], author, date, dateEnd])


def processAuthorEdges(aid1, aid2, pub_year):
    global edgesList

    year = int(pub_year.split('-')[0]);
    dateEnd = year_format.format(str(year + 1))

    date = pub_year
    #dateEnd = datetime.strptime(yearEnd, '%Y-%m-%d')
    #dateEnd = yearEnd.strftime('%Y-%m-%d')
    edgesList.append([aid1, aid2, date, dateEnd])

    # if len(authors) < 2:  # error checking, return if only one author for a publication
    #    return;
    #global dictAuthors;
    #global dictEdges;
    #index = 1;
    #numAuthors = len(authors);
    #auth_key_template = "{} {} {} {}"

    #journalRef = ''
    #if (journalReference is None):
    #    journalRef = ''
    #else:
    #    journalRef = journalReference.text

    #title = ''
    #if (paperTitle is None):
    #    title = ''
    #else:
    #    title = paperTitle.text

    #for auth in authors:
    #    if not ((auth is None) or (pubYear is None)):
    #        if len(auth) == 2:
    #            author = auth[1].text + " " + auth[0].text;
    #        elif len(auth) == 3:
    #            if "affiliation" in auth[2].tag:
    #                author = auth[1].text + " " + auth[0].text;
    #            else:
    #                author = auth[1].text + " " + auth[0].text + " " + auth[2].text;
    #        else:
    #            author = auth[0].text;


    #        for num in range(index, numAuthors):  # iterate through all co authors
    #            if len(authors[num]) == 2:
    #                 coAuthor = authors[num][1].text + " " + authors[num][0].text;
    #             elif len(authors[num]) == 3:
    #                 if "affiliation" in authors[num][2].tag:
    #                     coAuthor = authors[num][1].text + " " + authors[num][0].text;
    #                 else:
    #                     coAuthor = authors[num][1].text + " " + authors[num][0].text + " " + authors[num][2].text;
    #             else:
    #                 coAuthor = authors[num][0].text;
    #
    #             if (author > coAuthor):  # auth comes behind alphabetically
    #                 firstAuth = coAuthor;
    #                 secondAuth = author;
    #             else:
    #                 firstAuth = author;
    #                 secondAuth = coAuthor;
    #
    #             authKey = auth_key_template.format(dictAuthors[firstAuth], dictAuthors[secondAuth], date, dateEnd)
    #             if not authKey in dictEdges:  # check if edge record already exists
    #
    #                 dictEdges.update({authKey: [year]});
    #     index = index + 1;

def writeRecordsNodes():
    print nodesList[0]
    print nodesList[1]
    print nodesList[2]
    df = sqlContext.createDataFrame(nodesList, ["vid", "name", "estart", "eend"])
    df.saveAsParquetFile('./dblpNodes.paraquet')


def writeRecordsEdges():
    df = sqlContext.createDataFrame(edgesList, ["vid1", "vid2", "estart", "eend"])
    df.saveAsParquetFile('./dblpEdges.paraquet')

if __name__ == "__main__":
    if (not len(sys.argv) > 1):
        print ("Error: please provide the root directory of the nodes and edges files to be parsed")
        exit()
    else:
        arg1 = sys.argv[1]
        main(arg1)

