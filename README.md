# GraphXT-Parser

This project contains the python programs that are used to parse the datasets used by the DB Group for the Temporal Graph Project. This project contains parsers for the dblp, nGrams and ukDELIS datasets. The source files in this repository are written in python. The parsers provided are described below

Project Evolution:
In the early stages of the Temporal Graph Project, we used 2 formats for feeding the data in our program. The first dataset that was tested with the Temporal Graph project was the DBLP dataset. As such, the DBLP parsers provided in this repository provide the output data in two formats. The data is outputted in both nodes and edges format, as such there are 2 parsers each for nodes and for edges.
The 2 data formats provided are described as set1 and set2 respectively. Each format is described below:

Set1: [**** This format is no longer used ****]
Nodes file format: node-id,node-attribute,year1,year2,year3... year?
Edges file format: src-id dst-id year

Set2:
Nodes files format (one file per year): node-id,node-attribute
Edges files format (one file per year): src-id dst-id

Examples:
Nodes set1: 265683,Christophe Calvès,2008,2010,2013,2011,2014,2007
Edges set1: 3 4 1998
Nodes set2 (e.g. 2008 or 2010): 265683,Christophe Calvès
Edges set2 (e.g. 1998): 3 4

# DBLP Dataset
Source - http://dblp.uni-trier.de/xml/
Notes: 
    - To use the parsers provided, the document type definition, DTD (also provided at the link above as 'dblp.dtd') must be copied into the xml document (dblp.xml) using the standard internal subset declaration format of xml (see http://en.wikipedia.org/wiki/Document_type_definition for example).
    - Results of the parsers are outputted to the src/DBLP/results directory
    - The parsers are located in src/DBLP

Parsers provided (4):
    - nodes-set1.py (output to Nodes-set1.txt)
    - edges-set1.py (output to Edges-set1.txt)
    - nodes-set2.py (output to nodes dir with one node file for each year, example name format: nodes2008.txt)
    - edges-set2.py (output to edges dir with one edge file for each year, example name format: edges2008.txt)

To run the parsers from the command line, you may use the example commands:
    
    python nodes-set1.py /path-to-file/dblp.xml
    python edges-set1.py /path-to-file/dblp.xml /path-to-file/Nodes-set1.txt 
    
    python nodes-set2.py /path-to-file/Nodes-set1.txt ../../util/yearsDBLP.txt
    python edges-set2.py /path-to-file/Nodes-set1.txt ../../util/yearsDBLP.txt
    
    ** Note: the Nodes-set1.txt file referenced above is the output file from nodes-set1.py

** Additional Notes: 
    - the dblp.xml file is very large and takes some time to parse with the python programs provided. You can test the programs against the util/test.xml file provided, which contains a small set of the data contained in dblp.xml. Run the test with the following command:
  python dblp-parser-edges.py /path-to-directory/utils/test.xml
    - it is recommended to run the 'mkdir -p results/set2/nodes' and 'mkdir -p results/set2/edges' from src/DBLP in order to create the required directories for output files. Alternatively, you can change the location for output files.

# nGrams Dataset
Source - http://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html (English 1 million)
Notes: 
    - Due to the format of the raw data provided, we first create a "nodes dictionary," a listing of all nodes along with an assigned id number. The node-id pairs are used to further generate the nodes and edges files needed for the Temporal Graph project
    - We found that there isn't 100% correlation between words (nodes) used in the biarcs and arcs files provided. This means that, without additional precaution it is possible for a node to exist in a edge relationship with another node but not be documented as a node that exists by itself.
        ** for example: if the phrase "complete program" is occurred in 2009, we expect that it is also documented that the words "complete" and "program" also occured in 2009, however this was sometimes not the case.
            ** to resolve this problem, an additional parser, check-edges-set2.py is provided to check that all listed edge ids are also listed in the corresponding node files
    - This dataset also provides data on edge attributes, that is all years in which a pair of words (biarc) existed together. For this reason, the edges-set1-attr.py and edges-set2-attr.py parsers were created to output edge data along with edge attributes
    - Results of the parsers are outputted to the src/nGrams/results directory
    - The parsers are located in src/nGrams

Format for edges-set1-attr.py: srcId dstId year numOccur e.g. 3 4 2010 67
Format for edges-set2-attr.py (one per year e.g. edges2010.txt): srcId dstId numOccur e.g. 3 4 67

Parsers provided (6):
    - nodes-create-ids.py (output to nodesDict.txt i.e listing of all nodes with assigned id) 
    - nodes-set1.py (output to Nodes-set1.txt)
    - edges-set1-attr.py (output to Edges-set1-attr.txt)
    - nodes-set2.py (output to nodes dir with one node file for each year) 
    - edges-set2-attr (output to edges dir with one edge file for each year)
    - check-edges-set2.py (modifies nodes files generated by nodes-set2.py to append previously undocumented ids existing in corresponding edge files)

To run the parsers from the command line, you may use the example commands:
    
    python nodes-set1.py /path-to-results-directory/ /path-to-arcs-files/ /path-to-file/nodesDict.txt 
    python edges-set1-attr.py /path-to-results-directory/ /path-to-arcs-files/ /path-to-file/nodesDict.txt  

    python nodes-set2.py /path-to-results-directory/ /path-to-file/nodesDict.txt ../../util/yearsNGrams.txt
    python edges-set2-attr.py /path-to-results-directory/ /path-to-biarcs-files/ /path-to-file/nodesDict.txt ../../util/yearsNGrams.txt

    python nodes-create-ids.py /path-to-results-directory/ /path-to-biarcs-files/
    python check-edges-set2.py /path-to-file/nodesDict.txt ./path-to-dir/set2/nodes/nodes /path-to-dir/set2/edges/edges

** Additional Notes:
    - it is recommended to run the 'mkdir -p results/set2/nodes' and 'mkdir -p results/set2/edges' from src/DBLP in order to create the required directories for output files. Alternatively, you can change the location for output files.

# ukDELIS Dataset
Source - http://law.di.unimi.it/webdata/uk-union-2006-06-2007-05/
Notes:
    - the edge listing files provided in this dataset are very large, ~ 50gb each with 13 of such files. In order to parse these files, each one was split into 35 files and then read simultaneously with a program that spuns 12 threads.
    - the raw edge listing files provided already fit our desired format for edges, as such, the parsers provided here only edge the edge listing files to retrieve unique ids of nodes that exist in those files.
    - In a similar manner to the nGrams dataset, it was necessary to first generate a nodes dictionary to assign unique ids for each url provided at: http://data.law.di.unimi.it/webdata/uk-union-2006-06-2007-05/uk-union-2006-06-2007-05.urls.gz
    - The parsers are located in src/ukDELIS

Parsers provided (2):
    - nodes-create-ids.py (output to nodesDict.txt i.e listing of all nodes with assigned id) 
    - get-uniq-nodes-t.py (output to uniqNodes dir with one node file for each year)

To run the parsers from the command line, you may use the example commands:

    python nodes-create-ids.py /path-to-results-directory/ /path-to-ukDelis-url-listings/
    python get-uniq-nodes-t.py year-month /path-to-ukDELIS-edges-file/ /path-to-file/nodesDict.txt /path-to-results-directory/

    