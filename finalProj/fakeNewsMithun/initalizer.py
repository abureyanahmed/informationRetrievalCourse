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
from utils.process_input_data import cosine_sim
from utils.process_input_data import calculate_tf_idf
from utils.score import report_score, LABELS, score_submission
from sklearn.feature_extraction.text import TfidfTransformer
from csv import DictReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.fileWriter import writeToOutputFile
from utils.fileWriter import appendToFile

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


    #trying using tfidfvectorizer instead of tokenizing and tf-idf separately
    # tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    # tfs = tfidf.fit_transform(d.articles.values())
    # print(tfs.toarray())
    # print("number of linesin tfidf is:" + str(len(tfs.toarray())))


    # corpus = ['This is the first document.','This is the second second document.','And the  third third third one.','Is this the first document?',]
    # body_tokenized= tokenize(corpus)
    #
    # print(body_tokenized.toarray())

    # body_tokenized= tokenize(d.articles.values())
    # print("done tokenizing, number of rows in the tokenized vector is" + str(len(body_tokenized.toarray())))
    # print("done tokenizing, going to calculate tf-idf")
    # #give the counts/frequencies of terms to calculate tf-idf of the document
    # my_tf_idf_score_body= calculate_tf_idf(body_tokenized)
    # print(my_tf_idf_score_body.toarray())
    # print("number of lines in tf-idf is:" + str(len(my_tf_idf_score_body.toarray()[0])))
    #
    #
    writeToOutputFile("\n","cosSimScore_Stance")

    unrelated_biggest=0
    #for each headline, get the actual headline text
    for s in d.stances:
        #for each headline, get the actual headline text
        #print(s['Headline'])
        headline = s['Headline']
        #headline="a little bird"


        #get the corresponding body id for this headline
        bodyid  = s['Body ID']
        stance= s['Stance']

        #using that body id, retrieve teh corresponding article
        actualBody=d.articles[bodyid]
        cos=cosine_sim(actualBody,headline)
        appendToFile("bodyid:"+str(bodyid)+"\tcosine similarity:"+str(round(cos,3))+"\tgold label:"+stance+"\theadline:"+headline,"cosSimScore_Stance")
        appendToFile("\n","cosSimScore_Stance")

        if(stance=="unrelated"):
            #if its cosine sime value is bigger than the unrelated_biggest value so far, replace this value. This is to find the threshold
            #beyond which we want to call it related

            if(cos>unrelated_biggest):
                unrelated_biggest=cosine_sim(actualBody,headline)
                print ("unrelated_biggest:"+str(unrelated_biggest))



print ("done finding cosine similarity")
print("the value of maximum unrelated similarity is "+ str(unrelated_biggest))

# headline = s['Headline']
#         #headline="a little bird"
#
#
#         #get the corresponding body id for this headline
#         bodyid  = d.stances[0]['Body ID']
#         stance= d.stances[0]['Stance']
#
#         #using that body id, retrieve teh corresponding article
#         actualBody=d.articles[bodyid]
#         #actualBody= "a big bird barks"
#
#
#
#         print cosine_sim(actualBody,headline)

    # #give that headline to a tokenizer
    # headline_tokenized= tokenize(headline)
    #
    # #give that tokenized headline to tf-idf calculator
    # tf_idf_headline= calculate_tf_idf(headline_tokenized)

# #give that body to a tokenizer
    # body_tokenized= tokenize(actualBody)
    # #give that tokenized body to tf-idf calculator
    # tf_idf_body= calculate_tf_idf(body_tokenized)
    #
    # #calculate cosine similarity between headlines and body.
    #     cosine = cosine_similarity(tf_idf_body, tf_idf_headline, dense_output=True)
    # print cosine
    #
    #
    #
    #

