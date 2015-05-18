import sys;
import os;
import re;
import glob;
import collections;

#author: Halima Olapade
#date: May 2015
#example output: format 'nodeID,node,month1,month2'

dictUrls = collections.OrderedDict();
dictYears = collections.OrderedDict();
resultFileN = '/results/Nodes-ID.txt';

def parse(resultsPath, dirPath, nodesFileN):
    global dictUrls;
    global dictYears;    
    global resultFileN;
    
    print "Beginning program to parse file and create node listings for nodes, ids and months of occurence\n"

    resultFileN = resultsPath + resultFileN

    #load and initialize id-to-url map
    with open(nodesFileN, 'r') as nodeFile:
        for line in nodeFile:
            vars = line.split(',');
            id = int(vars[0]);
            url = vars[1].strip('\n');
            dictUrls[id] = url;
            dictYears.update({id : []});
        
            #print id," ",url

            for year in range(2, len(vars)):
                dictYears[id].append(year)
  
        #for a,b in dictYears.iteritems():
         #   print a," ",b           
    
    try:
        os.remove(resultFileN);
    except OSError:
        pass;


    #parse all files in the given directory
    for fileN in glob.glob(os.path.join(dirPath, '*')):
        r = re.compile('uk-(.*?).edges')
        m = r.search(fileN)
        timeInt = ""        

        if m:
            timeInt = m.group(1).replace("-", "")
        else:
            print "Found a file that is not an edges file:", fileN
            continue;

        with open(fileN, "r") as file:
            print("Current file: " + file.name)
        
            for line in file:
                args = line.split("\t");
                id1 = int(args[0])
                id2 = int(args[1].strip("\n"))

                #print id1,id2
        
                if not timeInt in dictYears[id1]:
                    dictYears[id1].append(timeInt) 
                
                if not timeInt in dictYears[id2]:
                    dictYears[id2].append(timeInt)    
    writeRecords();                

def writeRecords():
    resultFile = open(resultFileN, "w");

    for id, yrList in dictYears.iteritems():
        url = dictUrls[id];
        output = str(id) + "," + url + "," + ','.join(map(str, yrList));
        resultFile.write(output + "\n");
    resultFile.close();               

def main():
    if (not len(sys.argv) > 3):
        print ("Error: you must provide path to results dir, a directory containing txt files to read from and nodes dictionary");
        exit();
    else:
        arg1 = sys.argv[1];
        arg2 = sys.argv[2];
        arg3 = sys.argv[3];
        parse(arg1, arg2, arg3);


if __name__ == "__main__":
    main()
