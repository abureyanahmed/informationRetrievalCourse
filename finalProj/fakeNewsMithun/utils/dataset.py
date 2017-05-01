from csv import DictReader
import os
import sys

class DataSet():
    def __init__(self, cwd):

        #cwd = os.getcwd()
        #print("inside DataSet, current directory is:" + cwd)
        self.path = cwd+"/src/"
        #print("inside DataSet, current path is:" + self.path)
        print("Reading dataset")
        bodies = "train_bodies_original.csv"
        stances = "test_stances_csc483583.csv"

        self.stances = self.read(stances)
        articles = self.read(bodies)
        self.articles = dict()

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

        print("Number of Total stances: " + str(len(self.stances)))
        print("and the stances are : " + self.stances)
        print("Total bodies: " + str(len(self.articles)))



    def read(self,filename):
        rows = []
        with open(self.path + "/" + filename, "r", encoding='utf-8') as table:
            r = DictReader(table)
            for line in r:
                rows.append(line)
        return rows
