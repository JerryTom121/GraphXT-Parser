#GraphtXT-Parser

This project contains the python programs that are used to parse the datasets used by the DB Group for the Temporal Graph Project. This project contains parsers for the dblp, nGrams and ukDELIS datasets. The source files in this repository are written in python. The parsers provided are described below

Project Evolution:
In the early stages of the Temporal Graph Project, we used 2 formats for feeding the data in our program. The first dataset that was tested with the Temporal Graph project was the DBLP dataset. As such, the DBLP parsers provided in this repository provide the output data in two formats. The data is outputted in both nodes and edges format, as such there are 2 parsers each for nodes and for edges.
The 2 data formats provided are described as set1 and set2 respectively. Each format is described below:

Set1:
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

DBLP Dataset
Source - http://dblp.uni-trier.de/xml/
Notes: To use the parsers provided, the document type definition, DTD (also provided at the link above as 'dblp.dtd') must be copied into the xml document (dblp.xml) using the standard internal subset declaration format of xml (see http://en.wikipedia.org/wiki/Document_type_definition for example).

The parsers are located in src/DBLP
Parsers provided (4):
    - nodes-set1.py
    - edges-set1.py
    - nodes-set2.py
    - edges-set2.py

** Results of the parsers are outputted to the src/DBLP/results directory

To run the parsers from the command line, you may use the example command:
    python nodes-set1.py /path-to-file/dblp.xml
    python edges-set1.py /path-to-file/dblp.xml /path-to-file/Node-ID.txt 
    python nodes-set2.py /path-to-file/dblp.xml /path-to-file/Node-ID.txt 
    python edges-set2.py /path-to-file/dblp.xml /path-to-file/Node-ID.txt 
    **Note: the Node-ID.txt file referenced above is the output file from nodes-set1.py

NOTE: the dblp.xml file is very large and takes some time to parse with the python programs provided. You can test the programs against the util/test.xml file provided, which contains a small set of the data contained in dblp.xml. Run the test with the following command:
  python dblp-parser-edges.py /path-to-directory/utils/test.xml