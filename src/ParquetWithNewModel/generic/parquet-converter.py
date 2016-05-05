from datetime import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import sys

# lists for all nodes and edges
nodesList = []
edgesList = []

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
    #reading edges files
    for yr in range(min_year, max_year):
        pub_year = year_format.format(str(yr))
        filepath = edges_file_format.format(root, pub_year)

        print ("[info] edges file:", filepath)
        with open(filepath, 'r') as fd:
            for line in fd:
                args = line.strip("\n").split(" ")
                aid1 = int(args[0])
                aid2 = int(args[1])
                processAuthorEdges(aid1, aid2, pub_year)

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
    nodesList.append([aid, author, date, dateEnd])

def processAuthorEdges(aid1, aid2, pub_year):
    global edgesList

    year = int(pub_year.split('-')[0]);
    dateEnd = year_format.format(str(year + 1))

    date = pub_year
    edgesList.append([aid1, aid2, date, dateEnd])

def writeRecordsNodes():
    #print nodesList[0]
    #print nodesList[1]
    df = sqlContext.createDataFrame(nodesList, ["vid", "name", "estart", "eend"])
    df.saveAsParquetFile('./dblpNodes.paraquet')


def writeRecordsEdges():
    #print edgesList[0]
    #print edgesList[1]
    df = sqlContext.createDataFrame(edgesList, ["vid1", "vid2", "estart", "eend"])
    df.saveAsParquetFile('./dblpEdges.paraquet')

if __name__ == "__main__":
    if (not len(sys.argv) > 1):
        print ("Error: please provide the root directory of the nodes and edges files to be parsed")
        exit()
    else:
        arg1 = sys.argv[1]
        main(arg1)

