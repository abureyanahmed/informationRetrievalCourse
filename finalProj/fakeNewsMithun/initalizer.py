import os
import re
import nltk
from sklearn import feature_extraction
from tqdm import tqdm
import sys, webbrowser
import numpy
from sklearn.ensemble import GradientBoostingClassifier


from csv import DictReader


class DataSet():
    def __init__(self, path=""):
        self.path = path

        print("Reading the training dataset")
        bodies = "train_bodies_original.csv"
        stances = "train_stances_csc483583.csv"

        articles = self.read(bodies)
        self.stances = self.read(stances)

        self.articles = dict()

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

        print("Total stances: " + str(len(self.stances)))
        print("Total bodies: " + str(len(self.articles)))



    def read(self,filename):
        rows = []
        with open(self.path  + filename, "r", encoding='utf-8') as table:
            r = DictReader(table)

            for line in r:
                rows.append(line)
        return rows


#main code starts here

#cwd = os.getcwd()
#print("current directory is:"+cwd)
# Now change the directory

   # os.chdir( path )

if __name__ == "__main__":
    #read the data first
    d = DataSet()
