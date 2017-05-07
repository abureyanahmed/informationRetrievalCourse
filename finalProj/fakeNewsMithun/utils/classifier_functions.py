from __future__ import division
from utils.fileWriter import appendToFile
from utils.process_input_data import cosine_sim
import numpy as np
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import sys
from utils.process_input_data import tokenize
from utils.score import report_score

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
        #print("body_id:"+str(bodyid))
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

def predict_data_phase1(d, unrelated_threshold):
    total_pairs=0
    TP=FP=FN=TN=0
    goldlabel=""
    correct_prediction=0

    #note here we say related=0 and unrelated=1

    gold_predicted_combined=[[],[]]
    # actual = [0,0,0,0,1,1,0,3,3]
    # predicted = [0,0,0,0,1,1,2,3,3]

    for s in d.stances:
        total_pairs=total_pairs+1
        gold_int= []
        predicted_int= []
        #for each headline, get the actual headline text
        #print(s['Headline'])
        headline = s['Headline']
        #headline="a little bird"

        gold_predicted_this=[]
        #get the corresponding body id for this headline
        bodyid  = s['Body ID']
        stance= s['Stance']

        #using that body id, retrieve teh corresponding article
        actualBody=d.articles[bodyid]
        cos=cosine_sim(actualBody,headline)
        if(cos < unrelated_threshold ):
            pred_label="unrelated"
            predicted_int.append(1)
        else:
            pred_label="related"
            predicted_int.append(0)

        #rename gold label if its either of agree,disagree or discuss
        if(stance!="unrelated"):
            goldlabel="related"
            gold_int.append(0)
        else:
            goldlabel="unrelated"
            gold_int.append(1)

        gold_predicted_combined.append(gold_int)
        gold_predicted_combined.append(predicted_int)


    return gold_predicted_combined

# def split_phase1_predicted_data__related_unrelated
# This is a useless function. because. earlier i thought i had to train my phase2 bsed on predictions from phase 1.
def split_phase1_predicted_data__related_unrelated(data, unrelated_threshold):

    total_pairs=0
    TP=FP=FN=TN=0
    goldlabel=""
    correct_prediction=0

    #create a datasstructure of [headline, body, label]- matrix/2d array of strings.
    #Eg:
    #this guy related_rows will contain a list of headline_body_label_post_phase1_rows=[]
    #each headline_body_label_post_phase1_rows=[] will be an array of strings
    # [headline1, body1, stance1]
    # [headline2, body2, stance2]
    # [headline3, body3, stance3]

    related_matrix=[]


    for s in data.stances:
        total_pairs=total_pairs+1
        #for each headline, get the actual headline text
        #print(s['Headline'])
        headline = s['Headline']
        #headline="a little bird"


        #get the corresponding body id for this headline
        bodyid  = s['Body ID']
        stance= s['Stance']

        #using that body id, retrieve the corresponding article
        actualBody=data.articles[bodyid]

        #calculate cosine similarity
        cos=cosine_sim(actualBody,headline)
        if(cos < unrelated_threshold ):
            pred_label="unrelated"
        else:
            pred_label="related"



        #separate out teh 'related data' into another data set based on the predicted value
        #list of strings
        if(pred_label=="related"):
            headline_body_label=[]
            headline_body_label.append(headline)
            headline_body_label.append(actualBody)
            headline_body_label.append(pred_label)

        #append this headline_body_label guy to the big matrix
    related_matrix.append(headline_body_label)

    return related_matrix

def split_phase1_gold_data__related_unrelated(data):
    #create a datasstructure of [headline, body, label]- matrix/2d array of strings.
    #Eg:
    #this guy related_rows will contain a list of headline_body_label_post_phase1_rows=[]
    #each headline_body_label_post_phase1_rows=[] will be an array of strings
    # [headline1, body1, stance1]
    # [headline2, body2, stance2]
    # [headline3, body3, stance3]

    related_matrix=[]

    for s in data.stances:
        #total_pairs=total_pairs+1
        #for each headline, get the actual headline text
        #print(s['Headline'])
        headline = s['Headline']
        #headline="a little bird"

        #get the corresponding body id for this headline
        bodyid  = s['Body ID']
        stance= s['Stance']
        #using that body id, retrieve the corresponding article
        actualBody=data.articles[bodyid]


        #separate out teh 'related data' into another data set based on the predicted value
        #list of strings
        #print(stance)
        if(stance =="unrelated"):
            val=1
        else:
            headline_body_label=[]
            headline_body_label.append(headline)
            headline_body_label.append(actualBody)
            headline_body_label.append(stance)
            #append this headline_body_label guy to the big matrix
            related_matrix.append(headline_body_label)



    return related_matrix

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

def phase2_training_tf(data):
    print("inside phase2_training_tf")
    entire_corpus=[]
    labels = np.array([[]])
    #no_of_unrelated=0
    #feature_vector= np.array([[]])
    # feature_vector=feature_vector.reshape(-1, 1)
    # labels = np.array([[]])

    #just try creating a tf vector for one headline body combination.
    # [headline1, body1, stance1]

    for tuple in data:
        #print(str(tuple))

        headline_body_str=""
        headline = tuple[0]
        headline_body_str=headline_body_str+headline
        #bodyid  = tuple['Body ID']
        actualBody=tuple[1]
        headline_body_str=headline_body_str+actualBody
        entire_corpus.append(headline_body_str)

        stance= tuple[2]

        #lets call agrees as label 1 and disagrees as label 2
        if (stance == "agree"):
            labels = np.append(labels, 1)
        else:
            if (stance == "disagree"):
                labels = np.append(labels, 0)
            else:
                if(stance=="discuss"):
                    labels = np.append(labels, 2)






    print("size of entire_corpus is:" + str(len(entire_corpus)))
    print("going to vectorize teh related corpus :" )
    vectorizer = CountVectorizer(min_df=1)
    tf_vector = tokenize(entire_corpus)
    #print(tf_vector)
    print("number of rows in entire_corpus is:" + str(tf_vector.shape))
    print("going to feed this vectorized tf to a classifier:" )




    #feed the vectors to an an svm, with labels.
    clf = svm.SVC(kernel='linear', C=1.0)
    #feature_vector=feature_vector.reshape(-1, 1)
    clf.fit(tf_vector, labels.ravel())
    print("done training svm:" )
    return clf


def test_using_svm(test_data, svm_phase2):


    list_gold_label=[]
    entire_corpus=[]



    value2_int =2
    value1_int =1
    value0_int =0




    gold_predicted_combined=[[],[]]


    gold_int=[]
    for tuple in test_data:
        # headline = tuple[0]
        # actualBody=tuple[1]
        stance= tuple[2]

        # predicted_int=[]
        # entire_corpus.append(headline_body_str)
        headline_body_str=""
        headline = tuple[0]
        headline_body_str=headline_body_str+headline
        #bodyid  = tuple['Body ID']
        actualBody=tuple[1]
        headline_body_str=headline_body_str+actualBody
        entire_corpus.append(headline_body_str)

        #based on what the gold stance is, attach either 0,1,2 to gold label list
        #disagree=0
        #agree=1
        #discuss=2
        if (stance == "disagree"):
            gold_int.append(value0_int)
        else:
            if (stance == "agree"):
                gold_int.append(value1_int)
            else:
                if(stance=="discuss"):
                    gold_int.append(value2_int)
        #
        gold_predicted_combined.append(gold_int)
        #
        # headline_body_str=""
        # headline_body_str=headline_body_str+headline
        # headline_body_str=headline_body_str+actualBody
        #
        # print("going to vectorize headline_body_str :" )
        # vectorizer = CountVectorizer(min_df=1)
        # entire_corpus.append(headline_body_str)
        # tf_vector = tokenize(entire_corpus)
        # print(tf_vector)
        #
        # #give that vector to your svm for prediction.
        # pred_class=svm_phase2.predict(tf_vector)
        #
        # print("predicted class is:"+ str(pred_class[0]))
        #
        #
        #
        # if (pred_class[0] == value1 ):
        #     predicted_int.append(1)
        # else:
        #     if (pred_class[0] == value0 ):
        #         predicted_int.append(0)
        #     else:
        #         if (pred_class[0] == value2 ):
        #             predicted_int.append(2)
        # gold_predicted_combined.append(predicted_int)





    print("going to vectorize headline_body_str :" )
    vectorizer = CountVectorizer(min_df=1)

    tf_vector = tokenize(entire_corpus)
    #print(tf_vector)
    print("number of rows in entire_corpus is:" + str(tf_vector.shape))
    print("going to feed this vectorized tf to a classifier:" )

    print("going to predict class")
    #give that vector to your svm for prediction.
    pred_class=svm_phase2.predict(tf_vector)
    print("going to print pred_class")
    print("number of rows in pred_classis:" + str(pred_class.shape))
    #print(pred_class)


    #convert the predicted label to a regular list from numpy matrix

    pred_label_int=[]
    value2_float =2.0
    value1_float =1.0
    value0_float =0.0
    for x in np.nditer(pred_class):
        if(x==value2_float):
            pred_label_int.append(2)
        else:
            if(x==value1_float):
                pred_label_int.append(1)
            else:
                if(x==value0_float):
                    pred_label_int.append(0)




    print("total number of items in pred_label_int is:"+str(len(pred_label_int)))



    #print("going to find number of rows in gold_int:" )
    numrows = len(gold_int)    # 3 rows in your example
    #numcols = len(gold_int[0]) # 2 columns in your example
    print("number of rows in gold_int:" + str(numrows))
    #print("number of columns in gold_int:" + str(numcols))
    #print(gold_int)


    return gold_int, pred_label_int
    #return gold_int,gold_int


           # print("predicted:"+pred_label+"gold:"+goldlabel)



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

    print("number of lines in list_gold_label is "+ str(len(list_gold_label)))
    print("number of lines in pred_label is "+ str(len(list_pred_label)))
    print("first entry in list_gold_label is "+ str((list_gold_label[0])))
    print("first entry in pred_label is "+ str((list_pred_label[0])))
    print(classification_report(list_gold_label, list_pred_label))
    print("accuracy:"+str(accuracy_score(list_gold_label, list_pred_label)))
    print(report_score(list_gold_label,list_pred_label))
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
    return accuracy_score

