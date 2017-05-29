from csv import DictReader
import os
import sys
import csv


class load_training_DataSet_cs583():
    def __init__(self, cwd):

        #cwd = os.getcwd()
        #print("inside DataSet, current directory is:" + cwd)
        self.path = cwd+"/data/"
        #print("inside DataSet, current path is:" + self.path)
        #print("Reading dataset")
        bodies = "train_bodies_small.csv"
        stances = "train_stances_csc483583_small.csv"

        #print("going to read stances")

        #read the stances into a dictionary. Note that stances are in the format: Headline,Body ID,Stance
        self.stances = self.read(stances)
        #print("done reading stances")
       # print("going to read bodies")
        articles = self.read(bodies)
       # print("done reading bodies")
        self.articles = dict()
        #print("done creating dict")

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

       # print("Going to print all stances" )
       # print("Number of Total stances: " + str(len(self.stances)))
       # print("the first entry in stances is")
       # print(self.articles[0])
        #print("and the stances are : " + str(self.stances))
       # print("Total bodies: " + str(len(self.articles)))



    def read(self,filename):
        rows = []
        with open(self.path + "/" + filename, "rt") as table:
            #DictReader reads a csv into a dictionary format
            r = DictReader(table)
            for line in r:
                rows.append(line)
        return rows

class load_training_DataSet():
    def __init__(self, cwd,bodies, stances):

        #cwd = os.getcwd()
        #print("inside DataSet, current directory is:" + cwd)
        self.path = cwd+"/data/"
        #print("inside DataSet, current path is:" + self.path)
        #print("Reading dataset")
        #bodies = "train_bodies_small.csv"
        #stances = "train_stances_csc483583_small.csv"

        #print("going to read stances")

        #read the stances into a dictionary. Note that stances are in the format: Headline,Body ID,Stance
        self.stances = self.read(stances)
        #print("done reading stances")
       # print("going to read bodies")
        articles = self.read(bodies)
       # print("done reading bodies")
        self.articles = dict()
        #print("done creating dict")

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

       # print("Going to print all stances" )
       # print("Number of Total stances: " + str(len(self.stances)))
       # print("the first entry in stances is")
       # print(self.articles[0])
        #print("and the stances are : " + str(self.stances))
       # print("Total bodies: " + str(len(self.articles)))



    def read(self,filename):
        rows = []
        with open(self.path  + filename, "rt") as table:
            #DictReader reads a csv into a dictionary format
            r = DictReader(table)
            for line in r:
                rows.append(line)
        return rows


class load_testing_DataSet():
    def __init__(self, cwd,bodies, stances):

        #cwd = os.getcwd()
       # print("inside DataSet, current directory is:" + cwd)
        self.path = cwd+"/data/"
        #print("inside DataSet, current path is:" + self.path)
       # print("Reading dataset")
        #bodies = "train_bodies.csv"
        #stances = "test_stances_csc483583.csv"

        #print("going to read stances")

        #read the stances into a dictionary. Note that stances are in the format: Headline,Body ID,Stance
        self.stances = self.read(stances)
       # print("done reading stances")
       # print("going to read bodies")
        articles = self.read(bodies)
      #  print("done reading bodies")
        self.articles = dict()
      #  print("done creating dict")

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

        # print("Going to print all stances" )
        # print("Number of Total stances: " + str(len(self.stances)))
        # print("the first entry in stances is")
       # print(self.articles[0])
        #print("and the stances are : " + str(self.stances))
        #print("Total bodies: " + str(len(self.articles)))



    def read(self,filename):
        rows = []
        #ifile = open('sample.csv', "rt", encoding= < theencodingofthefile >)
        with open(self.path  + filename, "rt") as table:
            #DictReader reads a csv into a dictionary format
            r = DictReader(table)
            for line in r:
                rows.append(line)


        return rows



def read_lstm_data(path,filename):
    lstm_rows=[]
    with open(path+'lstm_output.txt', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
           # print("agree:"+row[0])
            lstm_rows.append(row)
    return lstm_rows

