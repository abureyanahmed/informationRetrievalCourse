import os
import re
import nltk
from sklearn import feature_extraction
from tqdm import tqdm
import sys, webbrowser
import numpy
from sklearn.ensemble import GradientBoostingClassifier
import utils;
import sys
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from utils.read_data import DataSet
from utils.process_input_data import tokenize
from utils.process_input_data import calculate_tf_idf
from utils.score import report_score, LABELS, score_submission
from sklearn.feature_extraction.text import TfidfTransformer
from csv import DictReader

#this is just the first file which has main function and strings together various sub modules.

if __name__ == "__main__":
    #make sure that the current working directory is the starting level
    # print("value of self.path is :"+ self.path)
    cwd = os.getcwd()
    print("current directory is:" + cwd)
    base_dir_name = os.path.dirname(os.path.abspath(sys.argv[0]))
    print("base directory is:" + base_dir_name)
    if(base_dir_name != cwd):
        os.chdir(base_dir_name)


    #read the data first
    cwd = os.getcwd()
    d = utils.read_data.DataSet(cwd)
    #print(d.stances)


    print("number of stances in d is"+str(len(d.stances)))
    print("number of bodies in d is"+str(len(d.articles)))
    print("done reading documents, going to tokenize this document")

    #print(d.articles(0))
    #print(d.articles[0])
    tokenizedData= tokenize(d.articles.values())

    print("done tokenizing, number of rows in the tokenized vector is"+str(len(tokenizedData.toarray())))
    print("done tokenizing, going to calculate tf-idf")

    # Create a term document index
    counts = [[3, 0, 1],[2, 0, 0],[3, 0, 0],[4, 0, 0],[3, 2, 0],[3, 0, 2]]

    #give the counts/frequencies of terms to calculate tf-idf of the document

    my_tf_idf_score_body= calculate_tf_idf(tokenizedData)
    #my_tf_idf_score=calculate_tf_idf(counts)


    print(my_tf_idf_score_body.toarray())
    print("number of linesin tfidf is:" + str(len(my_tf_idf_score_body.toarray())))




