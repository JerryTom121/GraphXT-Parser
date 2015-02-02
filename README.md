# DBLP-Parser
The source files in this repository are written in python. The parsers were written for the DBLP xml dataset (dblp.xml) provided at http://dblp.uni-trier.de/xml/

To use the parsers provided, the document type definition, DTD (also provided at the link above as 'dblp.dtd') must be copied into the xml document (dblp.xml) using the standard internal subset declaration format of xml (see http://en.wikipedia.org/wiki/Document_type_definition for example).

The parsers each output their results to a .txt document:
  - dblp_parser-nodes.txt outputs to "DBLPNodes.txt"
  - dblp_parser-edges.txt outputs to "DBLPEgdes.txt"

Note that the results outputted in the above files are not sorted in any particular order; you can use the unix 'sort' command to obtain alphabetical ordering of results.

To run the parsers from the command line, you may use the example command:
  python dblp-parser-edges.py /path-to-file/dblp.xml
