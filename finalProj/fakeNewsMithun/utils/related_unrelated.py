from __future__ import division
from utils.fileWriter import appendToFile
from utils.process_input_data import cosine_sim
import numpy as np
from sklearn import metrics
from sklearn import svm
#import matplotlib.pyplot as plt
#from matplotlib import style
#style.use("ggplot")

def calculateCosSimilarity(d):
    #writeToOutputFile("\n","cosSimScore_Stance")
    unrelated_biggest=0
    related_smallest=1
    correct_prediction=0
    total_pairs=0
    pred_label="related"

    for s in d.stances:
        total_pairs=total_pairs+1
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
            #below which we want to call it unrelated

            if(cos>unrelated_biggest):
                unrelated_biggest=cos

        else:
            #if its cosine sim  value is less than the related_smallest value so far, replace this value.
            # This is to find the threshold above which we want to call it related
            if(cos < related_smallest):
                related_smallest=cos

    print ("unrelated_biggest:"+str(unrelated_biggest))
    print ("related_smallest:"+str(related_smallest))
    return unrelated_biggest

def calculate_precision(d, unrelated_threshold):
    total_pairs=0
    TP=FP=FN=TN=0
    goldlabel=""
    correct_prediction=0

    for s in d.stances:
        total_pairs=total_pairs+1
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
        if(cos < unrelated_threshold ):
            pred_label="unrelated"
        else:
            pred_label="related"

        #rename gold label if its either of agree,disagree or discuss
        if(stance!="unrelated"):
            goldlabel="related"
        else:
            goldlabel="unrelated"


        if(pred_label=="unrelated"):
            if(pred_label==goldlabel):
                TN=TN+1
                correct_prediction=correct_prediction+1
            else:
                FN=FN+1
        else:
            if(pred_label==goldlabel):
                TP=TP+1
                correct_prediction=correct_prediction+1
            else:
                FP=FP+1


    print("TP:"+str(TP))
    print("FP:"+str(FP))

    print("TN:"+str(TN))
    print("FN:"+str(FN))

    recall=TN/(TN+FN)
    precision=TP/(TP+FP)
    print("precision:"+str(precision))
    print("recall:"+str(recall))
    #recall=TP/(TP+FP)
    accuracy=correct_prediction/total_pairs
    return accuracy


# This is from your training data. Now we will train only on the "related" ones
#  use this training data, to calculate cos similarity of each tuple and its gold label/stance
#. Feed that to an svm.
#Return: a classifier trained on  "related" tuples
def train_for_agree_disagree(d):

    no_of_unrelated=0
    feature_vector= np.array([[]])
    feature_vector=feature_vector.reshape(-1, 1)
    labels = np.array([[]])
    for s in d.stances:

        #for each headline, get the actual headline text
        headline = s['Headline']
        #headline="a little bird"


        #get the corresponding body id for this headline
        bodyid  = s['Body ID']
        stance= s['Stance']


        #WE are looking for stances which are only unrelated
        if(stance=="unrelated"):
            no_of_unrelated = no_of_unrelated + 1
        else:
            #i.e this is the group which has agree,disagree or discuss

            # using that body id, retrieve teh corresponding article
            actualBody = d.articles[bodyid]

            #find the cosine similarity between this body and headline
            cos = cosine_sim(actualBody, headline)
            feature_vector=feature_vector.reshape(-1, 1)
            feature_vector=np.append(feature_vector,[[cos]])

            #lets call agrees as label 1 and disagrees as label 2
            if (stance == "agree"):
                labels = np.append(labels, 1)
            else:
                if (stance == "disagree"):
                    labels = np.append(labels, 0)
                else:
                    if(stance=="discuss"):
                        labels = np.append(labels, 2)






    print("no_of_unrelated is:" + str(no_of_unrelated))
    print("number of rows in feature_vector is:"+str(len(feature_vector)))
    print("number of rows in labels is:" + str(len(labels)))
    #feed the vectors to an an svm, with labels.
    clf = svm.SVC(kernel='linear', C=1.0)
    feature_vector=feature_vector.reshape(-1, 1)
    clf.fit(feature_vector, labels.ravel())
    print("done training svm:" )
    return clf

def test_using_svm_calc_precision(test_data, svm):

    total_pairs=1
    TP=FP=FN=TN=1
    goldlabel=""
    correct_prediction=1
    pred_label=""

    list_pred_label=[]

    pred_label = ""
    # lets call agrees as label 1 and disagrees as label 2
    value2 =2.0
    value1 =1.0
    value0 =0.0



    for s in test_data.stances:


        total_pairs=total_pairs+1
        #for each headline, get the actual headline text

        headline = s['Headline']



        #get the corresponding body id for this headline
        bodyid  = s['Body ID']
        print("body id is:"+ str(bodyid))
        stance= s['Stance']

        if(stance!="unrelated"):
            #using that body id, retrieve teh corresponding article
            actualBody=test_data.articles[bodyid]
            cos=cosine_sim(actualBody,headline)

            print("cosine similarity of this tuple is:"+str(cos))
            cos_array=   [cos]
            temp = np.array(cos_array).reshape((1, -1))
            np.set_printoptions(precision=3)
            pred_class=svm.predict(temp)
            print("predicted class is:"+ str(pred_class[0]))




            if (pred_class[0] == value1 ):
                pred_label = "agree"
            else:
                if (pred_class[0] == value0 ):
                    pred_label = "disagree"
                else:
                    if (pred_class[0] == value2 ):
                        pred_label = "discuss"


            goldlabel=stance
            print("predicted:"+pred_label+"gold:"+goldlabel)

            list_pred_label.append(pred_label)

            # if(goldlabel=="agree"):
            #     if(pred_label=="agree"):
            #         TP = TP + 1
            #         correct_prediction=correct_prediction+1
            #     else:
            #         if(pred_label=="disagree"):
            #             FN=FN+1
            # if(goldlabel=="disagree"):
            #     if(pred_label=="disagree"):
            #         TN = TN + 1
            #         correct_prediction=correct_prediction+1
            #     else:
            #         if(pred_label=="agree"):
            #             FP=FP+1
    #
    # if (goldlabel == pred_label):
    #     if (pred_label == "agree"):
    #         TP = TP + 1
    #         correct_prediction = correct_prediction + 1
    #     else:
    #         if (pred_label == "disagree"):
    #             FN = FN + 1
    # if (goldlabel == "disagree"):
    #     if (pred_label == "disagree"):
    #         TN = TN + 1
    #         correct_prediction = correct_prediction + 1
    #     else:
    #         if (pred_label == "agree"):
    #             FP = FP + 1

    #end of for loop only 1 tab required

    classification_report(test_data.stances,)

    # print("TP:"+str(TP))
    # print("FP:"+str(FP))
    #
    # print("TN:"+str(TN))
    # print("FN:"+str(FN))
    #
    # recall=TN/(TN+FN)
    # precision=TP/(TP+FP)
    # print("precision:"+str(precision))
    # print("recall:"+str(recall))
    #
    # accuracy=correct_prediction/total_pairs
    # print("accuracy:" + str(accuracy))
    return accuracy

