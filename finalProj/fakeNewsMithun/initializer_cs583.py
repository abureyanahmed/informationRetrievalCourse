from __future__ import division
import nltk, string
import os
import sys;
import utils;
import csv;
import collections
import numpy as np
from utils.read_data import load_training_DataSet
from utils.classifier_functions import test_phase2_using_svm
from utils.classifier_functions import train_for_agree_disagree
from utils.classifier_functions import phase2_training
from utils.classifier_functions import phase2_training_hollywood
from utils.classifier_functions import calculateCosSimilarity
from utils.classifier_functions import calculate_precision
from utils.classifier_functions import return_related_data_only
from utils.classifier_functions import split_cos_sim
from utils.classifier_functions import split_phase1_gold_data_related_unrelated
from utils.classifier_functions import test_phase2_using_svm
from utils.classifier_functions import test_phase2_tf_hollywood
from utils.classifier_functions import predict_data_phase1
from utils.classifier_functions import convert_data_to_headline_body_stance_format
from utils.classifier_functions import predict_data_phase1_return_only_unrelated
from utils.classifier_functions import sendEmail
from utils.process_input_data import createAtfidfVectorizer
from utils.process_input_data import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
import itertools
from utils.process_input_data import doAllWordProcessing
from sklearn.feature_extraction.text import CountVectorizer
from utils.score import report_score
from utils.file_functions import writeToOutputFile
from utils.file_functions import appendToFile
from utils.process_input_data import my_lemmatize
from utils.read_data import read_lstm_data
from utils.read_data import load_testing_DataSet

import time


#in phase 1, we split teh data set to related- unrelated
do_training_phase1=False;
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
toaddr="mithunpaul08@gmail.com"
#toaddr="mithunpaul@email.arizona.edu"

start_time = time.time()
writeToOutputFile("start time:"+str(start_time), "logfile")

#or if its just 2 classes
#unrelated:0
#related=1
if __name__ == "__main__":
    try:

        #sys.exit(1)

        #nltk.download("wordnet", "whatever_the_absolute_path_to_myapp_is/nltk_data/")
       #print("number of arguments is"+ str(len(sys.argv)))




        if(len(sys.argv)>1):
            toaddr=sys.argv[1]

        ###########################-DO NOT DELETE###########################
        #--code for trainign related- unrelated class...this has to go in a if statement based on user input.
        #make sure that the current working directory is the starting level


        cwd = os.getcwd()
            # #print("current directory is:" + cwd)
        base_dir_name = os.path.dirname(os.path.abspath(sys.argv[0]))
        #print("base directory is:" + base_dir_name)
        if(base_dir_name != cwd):
            os.chdir(base_dir_name)



        # #Do training for 2 classes related-unrelated

       #print ("going to train on data for related-unrelated splitting aka phase1")

        #LOAD TRAINING DATA
        actual_phase1=[]
        predicted_phase1=[]
        actual_phase2=[]
        predicted_phase2 = []
        gold_phase1_only_unrelated= []
        predicted_phase1_only_unrelated= []

        unrelated_threshold=0

        #load their huge training data set
        #training_data = utils.read_data.load_training_DataSet(cwd)


        training_data = utils.read_data.load_training_DataSet(cwd,"train_bodies.csv","train_stances_csc483583.csv")
        testing_data = utils.read_data.load_testing_DataSet(cwd,"train_bodies.csv","test_stances_csc483583.csv")


        #lstm_output = read_lstm_data(base_dir_name + '/data/', 'lstm_output.txt')

        #load the smaller dataset which has only 2 entries
       # training_data = utils.read_data.load_training_DataSet(cwd,"train_bodies.csv","train_stances_csc483583_small.csv")
       # testing_data = utils.read_data.load_testing_DataSet(cwd,"train_bodies.csv","test_stances_csc483583_small.csv")

        #in validation phase, we test against the training data itself.
        #cwd = os.getcwd()

        coma = ","




        if(do_training_phase1):

            # #
            ##print("number of stances in d is" + str(len(training_data.stances)))
            ##print("number of bodies in d is" + str(len(training_data.articles)))
            ##print("done reading documents, going to tokenize this document")
            #
            #find the smallest value as the threshold
            #note: this works for the time being. have to replace it with svm
           #print ("done loading training data for phase 1. going to train the classifier ")
            unrelated_threshold= calculateCosSimilarity(training_data)
            # at this point you have a trained classifier. you can do two things now.
            #verify its accuracy against teh gold training data set or
            # directly use it on tewsting data
            #gold_predicted_combined=calculate_precision(training_data)





            cwd = os.getcwd()

           #print ("done with training of documents for phase1. going to start validation for phase 1")
            #sendEmail("do_training_phase1", toaddr)


            #########################This is the end of training for Phase1. Validation for phase 1 starts here###########################3
        if(do_validation_phase1):

            actual_phase1, predicted_phase1 =predict_data_phase1(training_data,unrelated_threshold)
            numrows_gold = len(actual_phase1)
            numrows_pred = len(predicted_phase1)
           #print ("total number of rows in gold matrix is:"+str(numrows_gold))
           #print ("total number of numcols in predicted matrix is:"+str(numrows_pred))
            #final_score=report_score([LABELS_RELATED[e] for e in actual_phase1],[LABELS_RELATED[e] for e in predicted_phase1])
            final_score=report_score([LABELS[e] for e in actual_phase1],[LABELS[e] for e in predicted_phase1])
            #sendEmail("do_validation_phase1")

    #        sys.exit(1)

    #########################This is the end of validation for Phase1. Training for phase 2 starts here###########################3

        if(do_training_phase2):
           #print("starting do_training_phase2")
            #split the gold data into related-unrelated class . you must train your svm2 on this new class



            #the string parameter lstm is just a dummy to separate two overloaded functions
            #related_data_gold_converted= split_phase1_gold_data_related_unrelated(training_data,"lstm")
            related_data_gold_converted = split_phase1_gold_data_related_unrelated(training_data)

            #related_data_gold_converted = convert_data_to_headline_body_stance_format(related_data_gold, lstm_output)


            #print("first .body  of testing_data_converted"+str(related_data_gold_converted[0].body ))
            ##print("first .headline  of testing_data_converted:" + str(related_data_gold_converted[2865].headline))
            ##print("first .body_id  of testing_data_converted:" + str(related_data_gold_converted[2865].body_id))
            ##print("first .predicted_stance  of testing_data_converted:" + str(related_data_gold_converted[2865].predicted_stance))
            ##print("first .gold_stance  of testing_data_converted:" + str(related_data_gold_converted[2865].gold_stance))
            ##print("first .unique_tuple_id  of testing_data_converted:" + str(related_data_gold_converted[2865].unique_tuple_id))
            ##print("first .confidence  of testing_data_converted:" + str(related_data_gold_converted[2865].confidence))
            ##print("first .agree_lstm  of testing_data_converted:" + str(related_data_gold_converted[2865].agree_lstm))
            ##print("first .disagree_lstm  of testing_data_converted:" + str(related_data_gold_converted[2865].disagree_lstm))
            ##print("first .discuss_lstm  of testing_data_converted:" + str(related_data_gold_converted[2865].discuss_lstm))
            ##print("first .unrelated_lstm  of testing_data_converted:" + str(related_data_gold_converted[2865].unrelated_lstm))


            # start training for 2 classes agree-disagree within related
           #print(" going to start training for 2 classes agree-disagree within related")

            vectorizer_phase2 = createAtfidfVectorizer()



            #this training has to be done on the gold training data split based on stance= related
           # svm_trained_phase2,vectorizer_phase2_trained=phase2_training_with_lstm(related_data_gold_converted,vectorizer_phase2)
           #  svm_trained_phase2, vectorizer_phase2_trained = phase2_training(related_data_gold_converted,
           #                                                                            vectorizer_phase2)

            svm_trained_phase2, vectorizer_phase2_trained = phase2_training_hollywood(related_data_gold_converted,
                                                                            vectorizer_phase2)




            #sys.exit(1)

           #print ("done with training of documents for agree classes. going to read testing data.")
            #sendEmail("do_training_phase2")

    #########################This is the end of training for Phase1. Validation for phase 2 starts here###########################3
        if(do_validation_phase2):


            entire_testing_data_converted=convert_data_to_headline_body_stance_format(testing_data)

           #print("number of rows in testing data after conversion is:"+str(len(testing_data_converted )))
           #print("number of columns in testing data after conversion is:"+str(len(testing_data_converted[0])))
           #print ("done loading testing data. going to test agree-disagree-discuss using the trained svm ")


            #test accuracy on the same data of 6000 related tuples
            #actual, predicted  = test_using_svm(related_data_gold, svm_trained_phase2)

            actual_phase2, predicted_phase2  = test_phase2_using_svm(entire_testing_data_converted, svm_trained_phase2, vectorizer_phase2_trained)

           #print ("done classifying testing data for phase 2. going to find score ")
            #sendEmail("do_validation_phase2")

    #########################This is the end of validation for Phase 2. Testing for Phase 1 starts here###########################3
        if(do_testing_phase1):


           #print("starting do_testing_phase1")
            #in testing phase, we first load the test data for the very first time.

            cwd = os.getcwd()

           #print ("done with training of documents for phase1. going to start testing for phase 1")
            unrelated_threshold=0.1

            #testing_data = utils.read_data.load_testing_DataSet(cwd)
            # load their huge testing data set

            # Then wesplit the test data based on the classifier trained on phase 1
            #print ("total number of rows in testing_data matrix is:"+str(len(testing_data.stances)))



            #we are also keeping teh gold_predicted data so that we can combine it for the final score calculation-after removing class "related" from
            #"both actual and predicted data"


            #below code is used as phase 2 input
           #print ("value of unrelated_threshold is:" + str(unrelated_threshold))
           #print("total number of rows in testing_data matrix is:" + str(len(testing_data.stances)))
           #print("total number of rows in testing_data matrix is:" + str((testing_data.stances)))

           # lstm_output = read_lstm_data(base_dir_name + '/data/', 'lstm_output.txt')
            entire_testing_data_converted = convert_data_to_headline_body_stance_format(testing_data)


            print("total number of rows in entire_testing_data_converted matrix is:" + str(len(entire_testing_data_converted)))

            print("self.predicted_stance = 0:" + str((entire_testing_data_converted[0].predicted_stance)))
            print("unique_tuple_id:" + str((entire_testing_data_converted[0].unique_tuple_id)))







           #print("going to predict data based on this new test set")
            # actual_phase1_only_unrelated, predicted_phase1_only_unrelated = predict_data_phase1_return_only_unrelated(
            #     training_data, unrelated_threshold)


           #print ("going to retreive only related data based on threshold:" + str(unrelated_threshold))

           #print ("total number of rows in testing_data_converted matrix is:"+str(len(testing_data_converted)))

           ##print(testing_data_converted)

           # print(entire_testing_data_converted)



            testdata_related_only, un_related_matrix, entire_testing_data_converted = split_cos_sim(entire_testing_data_converted, unrelated_threshold)
            #sendEmail("do_testing_phase1", toaddr)

            gold_phase1_only_unrelated=[]
            predicted_phase1_only_unrelated=[]

            for unr in un_related_matrix:
                gold_phase1_only_unrelated.append(unr.gold_stance)
                predicted_phase1_only_unrelated.append(unr.predicted_stance)

            # with open('my_output.csv', 'w', encoding='utf8') as f:
            #     field_names = ['Headline', 'Body ID', 'Stance', 'Confidence']
            #     spamwriter = csv.writer(f, delimiter=',')
            #     spamwriter.writerow(field_names)
            #
            # for eachTuple in un_related_matrix:
            #     if(eachTuple.predicted_stance==0):
            #         pred_label="agree"
            #     else:
            #         if(eachTuple.predicted_stance==1):
            #             pred_label="disagree"
            #         else:
            #             if (eachTuple.predicted_stance == 1):
            #                 pred_label = "disagree"
            #             else:
            #                 if (eachTuple.predicted_stance == 2):
            #                     pred_label = "discuss"
            #                 else:
            #                     if (eachTuple.predicted_stance == 3):
            #                         pred_label = "unrelated"
            #
            #     with open('my_output.csv', 'a+', encoding='utf8') as f:
            #         field_values=[eachTuple.headline,eachTuple.body_id,pred_label,eachTuple.confidence]
            #         spamwriter = csv.writer(f, delimiter=',')
            #         spamwriter.writerow(field_values)



            ##print("number of rows in actual_phase1_only_unrelated  is:" + str(len(gold_phase1_only_unrelated)))
            ##print("number of rows in predicted_phase1_only_unrelated  is:" + str(len(predicted_phase1_only_unrelated)))
            ##print("actual value of actual_phase1_only_unrelated  is:" + str((gold_phase1_only_unrelated[666])))
            ##print("actual value of in predicted_phase1_only_unrelated  is:" + str((predicted_phase1_only_unrelated[666])))

            #overwrite the file with an empty line if the file already exists
            #writeToOutputFile("\n", "enrique_format")

            #field_names = ['Headline', 'Body ID', 'Stance', 'Confidence']
            #writeToOutputFile("\n"+"Headline,Body ID,Stance,Confidence", "enrique_format")




                #
                # appendToFile("\n" + str(unr.headline) + coma, "enrique_format")
                # appendToFile(str(unr.body_id) + coma, "enrique_format")
                # appendToFile(str(unr.predicted_stance) + coma, "enrique_format")
                # appendToFile(str(unr.confidence), "enrique_format")

           #print("total number of rows in testdata_related_only matrix is:" + str(len(testdata_related_only)))


            #sys.exit(1)

            ######################### Testing for Phase 2 starts here###########################3

        if(do_testing_phase2):

           #print("\nstarting do_testing_phase2")
            #once the data is split into related-unrelated, we use the related data to split into 3






           #print ("total number of rows in testdata_related_only matrix is:"+str(len(testdata_related_only)))



            #print("number of lines in testing data is:"+str(len(testing_data. )))



            #entire_testing_data_converted=testdata_related_only;

           #print("number of rows in testing data after conversion is:"+str(len(testdata_related_only )))
            #print("number of columns in testing data after conversion is:"+str(len(testdata_related_only[0])))
           #print ("done loading testing data. going to test agree-disagree-discuss using the trained svm ")
           # actual_phase2, predicted_phase2  = test_phase2_using_svm(testdata_related_only, svm_trained_phase2, vectorizer_phase2_trained)
           # actual_phase2, predicted_phase2 = test_phase2_tf_hollywood(testdata_related_only, svm_trained_phase2,
            #                                                        vectorizer_phase2_trained)

            actual_phase2, predicted_phase2, post_prediction_data_phase2,entire_testing_data_converted = test_phase2_tf_hollywood(testdata_related_only,
                                                                                                    svm_trained_phase2,
                                                                                                    vectorizer_phase2_trained,entire_testing_data_converted)

           #print ("done classifying testing data for phase 2. going to find score ")

           #print("number of rows in actual_phase2  is:"+str(len(actual_phase2 )))
           #print(str(actual_phase2))

           #print("number of rows in predicted_phase2 is:"+str(len(predicted_phase2 )))
           #print(" of rows in predicted_phase2 is:" + str((predicted_phase2)))

           #print("number of rows in actual_phase1_only_unrelated  is:" + str(len(gold_phase1_only_unrelated)))
           #print("rows in actual_phase1_only_unrelated  is:" + str((gold_phase1_only_unrelated)))

           #print("number of rows in predicted_phase1_only_unrelated  is:"+str(len(predicted_phase1_only_unrelated )))
           #print("number of rows in predicted_phase1_only_unrelated  is:" + str((predicted_phase1_only_unrelated)))

            #combining results from both phases
            actual= gold_phase1_only_unrelated + actual_phase2
            predicted=predicted_phase1_only_unrelated+ predicted_phase2

            appendToFile(str("\nGold Labels:"), "logfile")
            appendToFile(str(actual), "logfile")
            appendToFile(str("\nPredicted Labels:"), "logfile")
            appendToFile(str(predicted), "logfile")

            final_score=report_score([LABELS[e] for e in actual],[LABELS[e] for e in predicted])

            appendToFile(str(final_score), "logfile")



            print("number of rows in entire_testing_data_converted  is:"+str(len(entire_testing_data_converted )))

            # #just logging code below
            #
            # with open('for_vikas.csv', 'w', encoding='utf8') as f:
            #     spamwriter = csv.writer(f, delimiter=',')
            #     spamwriter.writerow("\n")
            #
            # for vikas_tuple in entire_testing_data_converted:
            #     with open('for_vikas.csv', 'a+', encoding='utf8') as vikasfile:
            #         field_values_vikas=[vikas_tuple.predicted_stance]
            #         spamwriter = csv.writer(vikasfile, delimiter=',')
            #         spamwriter.writerow(field_values_vikas)
            #
            #
            # for eachTuple in post_prediction_data_phase2:
            #     # agree, disagree, or discuss, (0,1,2) and attach that.
            #     pred_label=""
            #     if(eachTuple.predicted_stance==0):
            #         pred_label="agree"
            #     else:
            #         if(eachTuple.predicted_stance==1):
            #             pred_label="disagree"
            #         else:
            #             if (eachTuple.predicted_stance == 1):
            #                 pred_label = "disagree"
            #             else:
            #                 if (eachTuple.predicted_stance == 2):
            #                     pred_label = "discuss"
            #                 else:
            #                     if (eachTuple.predicted_stance == 3):
            #                         pred_label = "unrelated"
            #
            #     with open('my_output.csv', 'a+', encoding='utf8') as f:
            #         field_values=[eachTuple.headline,eachTuple.body_id,pred_label,eachTuple.confidence]
            #         spamwriter = csv.writer(f, delimiter=',')
            #         spamwriter.writerow(field_values)




        elapsed_time = time.time() - start_time
        #print("time taken:" + str(elapsed_time))
        appendToFile("time taken:" + str(elapsed_time), "logfile")
        sendEmail("entire program", toaddr)


    except:
        import traceback
       #print('generic exception: ' + traceback.format_exc())
        # your code
        elapsed_time = time.time() - start_time
       #print("time taken:"+str(elapsed_time))
        sendEmail("inside try-catch. error occured, going to exit",toaddr)
