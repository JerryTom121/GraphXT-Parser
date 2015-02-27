# DBLP-Parser
The source files in this repository are written in python. The parsers were written for the DBLP xml dataset (dblp.xml) provided at http://dblp.uni-trier.de/xml/

To use the parsers provided, the document type definition, DTD (also provided at the link above as 'dblp.dtd') must be copied into the xml document (dblp.xml) using the standard internal subset declaration format of xml (see http://en.wikipedia.org/wiki/Document_type_definition for example).

Parsers provided (8):
- conf-edges.py (outputs to )
- conf-nodes.py (outputs to )
- dblp_parser-edges.py
- dblp_parser-nodes.py
- edges-id.py
- node-id.py
- normalized-edges.py
- normalized-nodes.py


Note that the results outputted in the above files are not sorted in any particular order; you can use the unix 'sort' command to obtain alphabetical ordering of results.



To run the parsers from the command line, you may use the example command:
  python dblp-parser-edges.py /path-to-file/dblp.xml

NOTE: the dblp.xml file is very large and takes some time to parse with the python programs provided. You can test the programs against the util/test.xml file provided, which contains a small set of the data contained in dblp.xml. Run the test with the following command:
  python dblp-parser-edges.py /path-to-directory/utils/test.xml
