from __future__ import division
import os
import sys;
import utils;
import numpy as np
from utils.read_data import load_training_DataSet
from utils.classifier_functions import test_phase2_using_svm
from utils.classifier_functions import train_for_agree_disagree
from utils.classifier_functions import phase2_training_tf
from utils.classifier_functions import calculateCosSimilarity
from utils.classifier_functions import calculate_precision
from utils.classifier_functions import return_related_data_only
from utils.classifier_functions import split_phase1_gold_data__related_unrelated
from utils.classifier_functions import test_phase2_using_svm
from utils.classifier_functions import predict_data_phase1
from utils.classifier_functions import convert_data_to_headline_body_stance_format
from utils.classifier_functions import predict_data_phase1_return_only_unrelated



from sklearn.feature_extraction.text import CountVectorizer
from utils.score import report_score



#in phase 1, we split teh data set to related- unrelated
do_training_phase1=True;
do_training_phase2=True;

do_validation_phase1=False;
do_validation_phase2=False;

do_testing_phase1=True;
do_testing_phase2=True;







LABELS = ['agree', 'disagree', 'discuss', 'unrelated']
LABELS_RELATED = ['unrelated','related']
RELATED = LABELS[0:3]

#acccording to FNC guys, this is the mapping of classes to labels
#agree:0
#disagree:1
#discuss:2
#unrelated:3


#or if its just 2 classes
#unrelated:0
#related=1
if __name__ == "__main__":

    ###########################-DO NOT DELETE###########################
    #--code for trainign related- unrelated class...this has to go in a if statement based on user input.
    #make sure that the current working directory is the starting level

    cwd = os.getcwd()
    print("current directory is:" + cwd)
    base_dir_name = os.path.dirname(os.path.abspath(sys.argv[0]))
    print("base directory is:" + base_dir_name)
    if(base_dir_name != cwd):
        os.chdir(base_dir_name)


    # #Do training for 2 classes related-unrelated
    # cwd = os.getcwd()
    print ("going to train on data for related-unrelated splitting aka phase1")

    #LOAD TRAINING DATA
    actual_phase1=[]
    predicted_phase1=[]
    actual_phase2=[]
    predicted_phase2 = []

    unrelated_threshold=0

    training_data = utils.read_data.load_training_DataSet(cwd)
    if(do_training_phase1):

        # #
        # print("number of stances in d is" + str(len(training_data.stances)))
        # print("number of bodies in d is" + str(len(training_data.articles)))
        # print("done reading documents, going to tokenize this document")
        #
        #find the smallest value as the threshold
        #note: this works for the time being. have to replace it with svm
        print ("done loading training data for phase 1. going to train the classifier ")
        unrelated_threshold= calculateCosSimilarity(training_data)
        # at this point you have a trained classifier. you can do two things now.
        #verify its accuracy against teh gold training data set or
        # directly use it on tewsting data
        #gold_predicted_combined=calculate_precision(training_data)





        cwd = os.getcwd()

        print ("done with training of documents for phase1. going to start validation for phase 1")


#########################This is the end of training for Phase1. Validation for phase 1 starts here###########################3
    if(do_validation_phase1):

        actual_phase1, predicted_phase1 =predict_data_phase1(training_data,unrelated_threshold)
        numrows_gold = len(actual_phase1)
        numrows_pred = len(predicted_phase1)
        print ("total number of rows in gold matrix is:"+str(numrows_gold))
        print ("total number of numcols in predicted matrix is:"+str(numrows_pred))
        #final_score=report_score([LABELS_RELATED[e] for e in actual_phase1],[LABELS_RELATED[e] for e in predicted_phase1])
        final_score=report_score([LABELS[e] for e in actual_phase1],[LABELS[e] for e in predicted_phase1])


        sys.exit(1)

#########################This is the end of validation for Phase1. Training for phase 2 starts here###########################3

    if(do_training_phase2):
        #split the gold data into related-unrelated class . you must train your svm2 on this new class

        related_data_gold= split_phase1_gold_data__related_unrelated(training_data)
        numrows = len(related_data_gold)
        numcols = len(related_data_gold[0])
        print ("total number of rows in related matrix is:"+str(numrows))
        print ("total number of numcols in related matrix is:"+str(numcols))




        # start training for 2 classes agree-disagree within related
        print(" going to start training for 2 classes agree-disagree within related")
        # cwd = os.getcwd()
        #training_data = utils.read_data.load_training_DataSet(cwd)

        # print("number of stances in d is" + str(len(training_data.stances)))
        # print("number of bodies in d is" + str(len(training_data.articles)))
        #print("done reading documents, going to train on this document")

        #this code was written before using term frequency as a feature vector. This uses cosine similarity of
        #q1d1 as a feature vector. This was first pass. got very bad precision. But leaving it here just in case the
        #2nd pass with term frequency as vector doesnt work and this will be back up option.
        #svm_trained_phase2 = train_for_agree_disagree(training_data)


        #use the same vectorizer for training and testing.
        vectorizer_phase2 = CountVectorizer(min_df=1)
        #this training has to be done on the gold training data split based on stance= related
        svm_trained_phase2,vectorizer_phase2_trained=phase2_training_tf(related_data_gold,vectorizer_phase2)

        print ("done with training of documents for agree classes. going to read testing data.")


#########################This is the end of training for Phase1. Validation for phase 2 starts here###########################3
    if(do_validation_phase2):

        #in validation phase, we test against the training data itself.
        cwd = os.getcwd()

        print ("done with training of documents for phase1. going to start testing for phase 1")
        testing_data = utils.read_data.load_testing_DataSet(cwd)
        # calculate_precision(training_data)
        #print("number of lines in testing data is:"+str(len(testing_data. )))

        #testing_data = utils.read_data.load_testing_DataSet(cwd)
        testing_data_converted=convert_data_to_headline_body_stance_format(testing_data)

        print("number of rows in testing data after conversion is:"+str(len(testing_data_converted )))
        print("number of columns in testing data after conversion is:"+str(len(testing_data_converted[0])))
        print ("done loading testing data. going to test agree-disagree-discuss using the trained svm ")


        #test accuracy on the same data of 6000 related tuples
        #actual, predicted  = test_using_svm(related_data_gold, svm_trained_phase2)

        actual_phase2, predicted_phase2  = test_phase2_using_svm(testing_data_converted, svm_trained_phase2, vectorizer_phase2_trained)

        print ("done classifying testing data for phase 2. going to find score ")

#########################This is the end of validation for Phase 2. Testing for Phase 1 starts here###########################3
    if(do_testing_phase1):

        print("starting do_testing_phase1")
        #in testing phase, we first load the test data for the very first time.

        cwd = os.getcwd()

        print ("done with training of documents for phase1. going to start testing for phase 1")


        testing_data = utils.read_data.load_testing_DataSet(cwd)

        # Then wesplit the test data based on the classifier trained on phase 1

        testdata_related_only=return_related_data_only(testing_data,unrelated_threshold)


        print ("total number of rows in testdata_related_only matrix is:"+str(len(testdata_related_only)))


        #we are also keeping teh gold_predicted data so that we can combine it for the final score calculation-after removing class "related" from
        #"both actual and predicted data"
        actual_phase1_only_unrelated, predicted_phase1_only_unrelated =predict_data_phase1_return_only_unrelated(training_data, unrelated_threshold)




######################### Testing for Phase 2 starts here###########################3

    if(do_testing_phase2):

        print("starting do_testing_phase2")
        #once the data is split into related-unrelated, we use the related data to split into 3



        #print("number of lines in testing data is:"+str(len(testing_data. )))


        testing_data_converted=convert_data_to_headline_body_stance_format(testdata_related_only)

        print("number of rows in testing data after conversion is:"+str(len(testing_data_converted )))
        print("number of columns in testing data after conversion is:"+str(len(testing_data_converted[0])))
        print ("done loading testing data. going to test agree-disagree-discuss using the trained svm ")
        actual_phase2, predicted_phase2  = test_phase2_using_svm(testing_data_converted, svm_trained_phase2, vectorizer_phase2_trained)

        print ("done classifying testing data for phase 2. going to find score ")

        #combining results from both phases
        actual=actual_phase1_only_unrelated+ actual_phase2
        predicted=predicted_phase1_only_unrelated+ predicted_phase2

        final_score=report_score([LABELS[e] for e in actual],[LABELS[e] for e in predicted])

