import urllib

urlBase = "http://data.law.di.unimi.it/webdata/"
prefix = "uk-"
gSuffix = ".graph" 
pSuffix = ".properties"

gTestfile = urllib.URLopener()
pTestfile = urllib.URLopener()

currentYear = 2006
startMonth = 5
endMonth = 13	

for i in range(0, 2):
	print "Downloading files for", currentYear

	
	for num in range(startMonth, endMonth):
		fileIndex = str(num); 

		if (num < 10):
			fileIndex = "0" + str(num);
		
		filePath = prefix + str(currentYear) + "-" + fileIndex + "/"
		gfileName = prefix + str(currentYear) + "-" + fileIndex + gSuffix
		pfileName = prefix + str(currentYear) + "-" + fileIndex + pSuffix
	
		gSavePath = "./data/graph/" + gfileName
		pSavePath = "./data/prop/" + pfileName
	
		gUrl = urlBase + filePath + gfileName
		pUrl = urlBase + filePath + pfileName
	
		print gUrl
		gTestfile.retrieve(gUrl, gSavePath)
		
		print pUrl
		pTestfile.retrieve(pUrl, pSavePath)
	currentYear = 2007
	startMonth = 1
	endMonth = 6

