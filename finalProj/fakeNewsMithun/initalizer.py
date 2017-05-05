from __future__ import division
import os
import utils;
import numpy as np
from utils.read_data import load_training_DataSet
from utils.related_unrelated import test_using_svm_calc_precision
from utils.related_unrelated import train_for_agree_disagree

#this is just the first file which has main function and strings together various sub modules.

if __name__ == "__main__":
    ###########################-DO NOT DELETE###########################
    # --code for trainign related- unrelated class...this has to go in a if statement based on user input.
    # make sure that the current working directory is the starting level
    # print("value of self.path is :"+ self.path)
    # cwd = os.getcwd()
    # print("current directory is:" + cwd)
    # base_dir_name = os.path.dirname(os.path.abspath(sys.argv[0]))
    # print("base directory is:" + base_dir_name)
    # if(base_dir_name != cwd):
    #     os.chdir(base_dir_name)
    #
    #
    # #Do training for 2 classes related-unrelated
    # cwd = os.getcwd()
    # training_data = utils.read_data.load_training_DataSet(cwd)
    #
    # print("number of stances in d is" + str(len(training_data.stances)))
    # print("number of bodies in d is" + str(len(training_data.articles)))
    # print("done reading documents, going to tokenize this document")
    #
    #
    # unrelated_threshold= calculateCosSimilarity(training_data)
    # #unrelated_threshold=0.399
    # # calculate_precision(training_data)
    #
    # print ("done with training of documents.starting testing")
    #
    # ### start of testing phase for 2 classes- related unrelated
    # cwd = os.getcwd()
    # testing_data = utils.read_data.load_testing_DataSet(cwd)
    # print ("done loading testing data. going to caculate accuracy")
    # accuracy = calculate_precision(testing_data, unrelated_threshold)
    # print ("accuracy:"+str(accuracy))

    #######################end of classification for  2 classes related-unrelated

    # start training for 2 classes agree-disagree within related
    print(" start training for 2 classes agree-disagree within related")
    cwd = os.getcwd()
    training_data = utils.read_data.load_training_DataSet(cwd)

    print("number of stances in d is" + str(len(training_data.stances)))
    print("number of bodies in d is" + str(len(training_data.articles)))
    print("done reading documents, going to train on this document")

    svm_trained = train_for_agree_disagree(training_data)
    # unrelated_threshold=0.399
    # calculate_precision(training_data)


    print ("done with training of documents for agree classes. going to read testing data.")



    testing_data = utils.read_data.load_testing_DataSet(cwd)
    print ("done loading testing data. going to test using the trained svm ")
    accuracy = test_using_svm_calc_precision(testing_data, svm_trained)
    print ("accuracy:"+str(accuracy))


