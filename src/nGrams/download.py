import urllib

urlBase = "http://commondatastorage.googleapis.com/books/syntactic-ngrams/eng-1M/"
prefix = "arcs."
suffix = "-of-99.gz" 
testfile = urllib.URLopener()

print "Downloading files from:"
for num in range(3, 99):
	fileIndex = str(num); 

	if (num < 10):
		fileIndex = "0" + str(num);
	
	fileName = prefix + fileIndex + suffix
	savePath = "./data/arcs/" + fileName
	url = urlBase + fileName
	print url
	testfile.retrieve(url, savePath)
