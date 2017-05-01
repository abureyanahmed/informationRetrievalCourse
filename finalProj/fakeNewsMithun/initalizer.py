import os
import re
import nltk
from sklearn import feature_extraction
from tqdm import tqdm
import sys, webbrowser
import numpy
from sklearn.ensemble import GradientBoostingClassifier
import utils;
import src.dataProcessing;
import sys
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from utils.dataset import DataSet
from utils.score import report_score, LABELS, score_submission
from sklearn.feature_extraction.text import TfidfTransformer
from csv import DictReader

#this is just the first file which has main function and strings together various sub modules.

if __name__ == "__main__":
    #make sure that the current working directory is the starting level
    # print("value of self.path is :"+ self.path)
    cwd = os.getcwd()
   # print("current directory is:" + cwd)
    base_dir_name = os.path.dirname(os.path.abspath(sys.argv[0]))
   # print("base directory is:" + base_dir_name)
    if(base_dir_name != cwd):
        os.chdir(base_dir_name)


    #read the data first
    cwd = os.getcwd()
    d = utils.dataset.DataSet(cwd)

    # Create a term document index
    counts = [[3, 0, 1],[2, 0, 0],[3, 0, 0],[4, 0, 0],[3, 2, 0],[3, 0, 2]]

    #give the counts/frequencies of terms to calculate tf-idf of the document
    objdp= src.dataProcessing.ProcessData()
    my_tf_idf_score=objdp.calculate_tf_idf(counts)
    print(my_tf_idf_score)




