
def writeToOutputFile(textToWrite,stubFilename):
    target = open(stubFilename+'.txt', 'w+')
    target.write(textToWrite);
    target.close()

def appendToFile(textToWrite,stubFilename):
    target = open(stubFilename+'.txt', 'a+')
    target.write(textToWrite);
    target.close()
