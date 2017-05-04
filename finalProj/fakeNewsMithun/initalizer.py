from __future__ import division
import os
import re

from csv import DictReader

import sys, webbrowser
import numpy
from sklearn.ensemble import GradientBoostingClassifier
import utils;
import sys


from sklearn.ensemble import GradientBoostingClassifier
from utils.read_data import load_training_DataSet
from utils.process_input_data import tokenize
from utils.process_input_data import cosine_sim
from utils.process_input_data import calculate_tf_idf
from utils.score import report_score, LABELS, score_submission
from sklearn.feature_extraction.text import TfidfTransformer
from csv import DictReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.fileWriter import writeToOutputFile
from utils.fileWriter import appendToFile
from utils.related_unrelated import calculateCosSimilarity
from utils.related_unrelated import calculateAccuracy

import nltk
import numpy as np
from sklearn import feature_extraction
from tqdm import tqdm
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


    #Do training
    # cwd = os.getcwd()
    # training_data = utils.read_data.load_training_DataSet(cwd)
    #
    # print("number of stances in d is" + str(len(training_data.stances)))
    # print("number of bodies in d is" + str(len(training_data.articles)))
    # print("done reading documents, going to tokenize this document")
    #

    #unrelated_threshold= calculateCosSimilarity(training_data)
    unrelated_threshold=0.399
    # calculateAccuracy(training_data)

    print ("done with training of documents.starting testing")

    ### start of testing phase
    cwd = os.getcwd()
    testing_data = utils.read_data.load_testing_DataSet(cwd)
    print ("done loading testing data. going to caculate accuracy")
    accuracy=calculateAccuracy(testing_data,unrelated_threshold)
    print ("accuracy:"+str(accuracy))

