from __future__ import division
import os
import numpy as np
import smtplib
import sys
import scipy
from sklearn import svm
import os
import re
import nltk
import numpy as np
from sklearn import feature_extraction
from tqdm import tqdm
import itertools
from utils.file_functions import writeToOutputFile
from utils.process_input_data import cosine_sim
from utils.feature_engineering import refuting_features, polarity_features, hand_features,hedging_features
from utils.feature_engineering import word_overlap_features
from tqdm import tqdm
from utils.datastructures import indiv_headline_body
from utils.process_input_data import createAtfidfVectorizer
import itertools
from utils.process_input_data import doAllWordProcessing
import os
import re
import nltk
import numpy as np
from sklearn import feature_extraction
from tqdm import tqdm
import os
import re
import nltk
import numpy as np
from sklearn import feature_extraction
from tqdm import tqdm

# from keras.layers.embeddings import Embedding
# from keras.layers.recurrent import LSTM
# from keras.layers.wrappers import Bidirectional
#
# ############# Using sentence similarity
# from Sent_similarity import similarity

#############

_wnl = nltk.WordNetLemmatizer()


LABELS = ['agree', 'disagree', 'discuss', 'unrelated']
LABELS_RELATED = ['unrelated','related']
RELATED = LABELS[0:3]

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

        # actualBody_lemmatized=[]
        #
        # wordnet_lemmatizer = WordNetLemmatizer()
        # for indivWord in actualBody:
        #     lem_word=wordnet_lemmatizer.lemmatize(indivWord )
        #     actualBody_lemmatized.append(lem_word)
        #
        # print(actualBody_lemmatized);

        cos=cosine_sim(actualBody,headline)


        #appendToFile("bodyid:"+str(bodyid)+"\tcosine similarity:"+str(round(cos,3))+"\tgold label:"+stance+"\theadline:"+headline,"cosSimScore_Stance")
        #appendToFile("\n","cosSimScore_Stance")

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

    #print ("unrelated_biggest:"+str(unrelated_biggest))
    #print ("related_smallest:"+str(related_smallest))
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

    value2_int =2
    value1_int =1
    value0_int =0
    value3_int =3
    value4_int =4

    #note here we say related=0 and unrelated=1
    gold_int= []
    predicted_int= []
    gold_predicted_combined=[[],[]]
    # actual = [0,0,0,0,1,1,0,3,3]
    # predicted = [0,0,0,0,1,1,2,3,3]

    for s in d.stances:
        total_pairs=total_pairs+1

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

        #unrelated:0
        #related=1
        if(cos < unrelated_threshold ):
            pred_label="unrelated"
            predicted_int.append(value0_int)
        else:
            pred_label="related"
            predicted_int.append(value1_int)

        #rename gold label if its either of agree,disagree or discuss
        if(stance=="unrelated"):
            goldlabel="unrelated"
            gold_int.append(value0_int)
        else:
            goldlabel="related"
            gold_int.append(value1_int)

        #gold_predicted_combined.append(gold_int)
        #gold_predicted_combined.append(predicted_int)


    return gold_int,predicted_int

#this is done so that the actual_predicted matrix can be combined with the output of phase 2
def predict_data_phase1_return_only_unrelated(d, unrelated_threshold):
    total_pairs=0

    value2_int =2
    value1_int =1
    value0_int =0
    value3_int =3
    value4_int =4

    #note here we say related=0 and unrelated=1
    gold_int= [0]
    predicted_int= [0]
    gold_predicted_combined=[[],[]]
    # actual = [0,0,0,0,1,1,0,3,3]
    # predicted = [0,0,0,0,1,1,2,3,3]

    for s in d.stances:
        total_pairs=total_pairs+1

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

        #unrelated:0
        #related=1
        if(cos < unrelated_threshold ):
            pred_label="unrelated"
            predicted_int.append(value3_int)

            #so it predicted that a value is unrelated. We need to retrieve its gold value
            #if its golden value, i.e stance is unrelated, attach a 3, else go find its actual label, i.e
            #agree, disagree, or discuss, (0,1,2) and attach that.
            if(stance=="unrelated"):
                gold_int.append(value3_int)
            else:
                if (stance == "agree"):
                    gold_int.append(value0_int)
                else:
                    if (stance == "disagree"):
                        gold_int.append(value1_int)
                    else:
                        if(stance=="discuss"):
                            gold_int.append(value2_int)
        else:
            pred_label="related"
            #dont do anything if the predicted label is related. we dont care about this set at this point.
            #right now we just want the results of unrelated prediction, so that we can feed it to their score calculator
    return gold_int,predicted_int


# def split_phase1_predicted_data__related_unrelated
# This will be used in test set, where the initial test set will be split into related adn unrelated group, based on teh
# prediction - note that only related data is being returned.
def return_related_data_only(data, unrelated_threshold):

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
        #this will be fed as input for the 2nd classifier
        #list of strings
        if(pred_label=="related"):

            # obj_indiv_headline_body = indiv_headline_body() ;
            # obj_indiv_headline_body.body_id = bodyid 
            # obj_indiv_headline_body.body = actualBody 
            # obj_indiv_headline_body.gold_stance = stance 
            # obj_indiv_headline_body.headline = headline 

            #headline_body_label = []
            # headline_body_label.append(headline)
            # headline_body_label.append(actualBody)
            # headline_body_label.append(stance)

            related_matrix.append(obj_indiv_headline_body)

        #append this headline_body_label guy to the big matrix


    return related_matrix

def split_cos_sim(testing_data_converted, unrelated_threshold):

    related_matrix=[]
    un_related_matrix = []

    print ("inside split_cos_sim")

    for indivDataTuple in testing_data_converted:

        headline = indivDataTuple.headline
        bodyid=indivDataTuple.body_id
        actualBody=indivDataTuple.body

        #calculate cosine similarity
        cos=cosine_sim(actualBody,headline)
        #print(cos)
        pred_int=3
        if(cos < unrelated_threshold ):
            pred_label="unrelated"
            pred_int = 3
        else:
            pred_label="related"
            pred_int=4


        indivDataTuple.predicted_stance=pred_int
        #separate out teh 'related entire_testing_data_converted' into another entire_testing_data_converted set based on the predicted value
        #this will be fed as input for the 2nd classifier
        if(pred_label=="related"):
            related_matrix.append(indivDataTuple)
        else:
            un_related_matrix.append(indivDataTuple)
            indivDataTuple.predicted_stance=3



    return related_matrix,un_related_matrix,testing_data_converted


def split_phase1_gold_data_related_unrelated(data):

    related_matrix=[]
    tuple_counter = 0

    #for stance, lstm_row in itertools.zip_longest(data.stances, ):
    for stance in data.stances:

        headline = stance['Headline']

        #get the corresponding body id for this headline
        bodyid  = stance['Body ID']
        stance= stance['Stance']

        #using that body id, retrieve the corresponding article
        actualBody=data.articles[bodyid]

        obj_indiv_headline_body = indiv_headline_body()
        obj_indiv_headline_body.body_id = bodyid
        obj_indiv_headline_body.headline = headline

        obj_indiv_headline_body.body = actualBody
        obj_indiv_headline_body.unique_tuple_id = tuple_counter

        #separate out teh 'related data' into another data set based on the golden value

    #initiate all lstm values to 0. this will turn to 1 based on its gold stance
        # obj_indiv_headline_body.agree_lstm = 0
        # obj_indiv_headline_body.disagree_lstm = 0
        # obj_indiv_headline_body.discuss_lstm = 0
        # obj_indiv_headline_body.unrelated_lstm =0

        if(stance =="unrelated"):
            val=1
        else:
            gold_stance_int = 0
            if (stance == "agree"):
                gold_stance_int = 0
               # obj_indiv_headline_body.agree_lstm = 1
            else:
                if (stance == "disagree"):
                    gold_stance_int = 1
                   # obj_indiv_headline_body.disagree_lstm = 1
                else:
                    if (stance == "discuss"):
                        gold_stance_int = 2
                       # obj_indiv_headline_body.discuss_lstm = 1
                    else:
                        #technically code should never reach here
                        if (stance == "unrelated"):
                            gold_stance_int = 3
                          #  obj_indiv_headline_body.unrelated_lstm = 1

            obj_indiv_headline_body.gold_stance = gold_stance_int
            related_matrix.append(obj_indiv_headline_body)
            tuple_counter = tuple_counter + 1

            # headline_body_label=[]
            # headline_body_label.append(headline)
            # headline_body_label.append(actualBody)
            # headline_body_label.append(stance)
            # #append this headline_body_label guy to the big matrix
            # related_matrix.append(headline_body_label)



    return related_matrix

#overloaded version which has lstm related feature vector generation.
def split_phase1_gold_data_related_unrelated_lstm(data,lstm):

    related_matrix=[]
    tuple_counter = 0

    #for stance, lstm_row in itertools.zip_longest(data.stances, ):
    for stance in data.stances:

        headline = stance['Headline']

        #get the corresponding body id for this headline
        bodyid  = stance['Body ID']
        stance= stance['Stance']

        #using that body id, retrieve the corresponding article
        actualBody=data.articles[bodyid]

        obj_indiv_headline_body = indiv_headline_body()
        obj_indiv_headline_body.body_id = bodyid
        obj_indiv_headline_body.headline = headline

        obj_indiv_headline_body.body = actualBody
        obj_indiv_headline_body.unique_tuple_id = tuple_counter

        #separate out teh 'related data' into another data set based on the golden value

    #initiate all lstm values to 0. this will turn to 1 based on its gold stance
        obj_indiv_headline_body.agree_lstm = 0
        obj_indiv_headline_body.disagree_lstm = 0
        obj_indiv_headline_body.discuss_lstm = 0
        obj_indiv_headline_body.unrelated_lstm =0

        if(stance =="unrelated"):
            val=1
        else:
            gold_stance_int = 0
            if (stance == "agree"):
                gold_stance_int = 0
                obj_indiv_headline_body.agree_lstm = 1
            else:
                if (stance == "disagree"):
                    gold_stance_int = 1
                    obj_indiv_headline_body.disagree_lstm = 1
                else:
                    if (stance == "discuss"):
                        gold_stance_int = 2
                        obj_indiv_headline_body.discuss_lstm = 1
                    else:
                        #technically code should never reach here
                        if (stance == "unrelated"):
                            gold_stance_int = 3
                            obj_indiv_headline_body.unrelated_lstm = 1

            obj_indiv_headline_body.gold_stance = gold_stance_int
            related_matrix.append(obj_indiv_headline_body)
            tuple_counter = tuple_counter + 1

            # headline_body_label=[]
            # headline_body_label.append(headline)
            # headline_body_label.append(actualBody)
            # headline_body_label.append(stance)
            # #append this headline_body_label guy to the big matrix
            # related_matrix.append(headline_body_label)



    return related_matrix


def convert_data_to_headline_body_stance_format(data,lstm_output):
    print("inside convert_data_to_headline_body_stance_format:")
    print(" of rows in testing_data matrix is:" + str((data.stances)))
    tuple_counter=0
    data_my_format=[]

    for stance, lstm_row in zip(data.stances, lstm_output):

#uncomment this line below if you want to run for the longer list
#        for stance,lstm_row  in itertools.zip_longest( data.stances, lstm_output):



        headline = stance['Headline']
        #print(headline)

        #get the corresponding body id for this headline
        bodyid  = stance['Body ID']
        stance= stance['Stance']

        gold_stance_int = 0
        if (stance == "agree"):
            gold_stance_int = 0
        else:
            if (stance == "disagree"):
                gold_stance_int = 1
            else:
                if (stance == "discuss"):
                    gold_stance_int = 2
                else:
                    if (stance == "unrelated"):
                        gold_stance_int = 3



        #using that body id, retrieve the corresponding article
        actualBody=data.articles[bodyid]

        obj_indiv_headline_body= indiv_headline_body()
        obj_indiv_headline_body.body_id=bodyid
        obj_indiv_headline_body.headline=headline
        obj_indiv_headline_body.gold_stance = gold_stance_int
        obj_indiv_headline_body.body = actualBody
        obj_indiv_headline_body.unique_tuple_id=tuple_counter
        obj_indiv_headline_body.agree_lstm = lstm_row[0]
        obj_indiv_headline_body.disagree_lstm = lstm_row[1]
        obj_indiv_headline_body.discuss_lstm = lstm_row[2]
        obj_indiv_headline_body.unrelated_lstm = lstm_row[3]

        tuple_counter=tuple_counter+1



        data_my_format.append(obj_indiv_headline_body)



    return data_my_format

#overloaded version which doesnt have lstm input
def convert_data_to_headline_body_stance_format(data):
    print("inside convert_data_to_headline_body_stance_format:")
    print(" of rows in testing_data matrix is:" + str((data.stances)))
    tuple_counter=0
    data_my_format=[]

    for stance in data.stances:

        headline = stance['Headline']
        #print(headline)

        #get the corresponding body id for this headline
        bodyid  = stance['Body ID']
        stance= stance['Stance']

        gold_stance_int = 0
        if (stance == "agree"):
            gold_stance_int = 0
        else:
            if (stance == "disagree"):
                gold_stance_int = 1
            else:
                if (stance == "discuss"):
                    gold_stance_int = 2
                else:
                    if (stance == "unrelated"):
                        gold_stance_int = 3



        #using that body id, retrieve the corresponding article
        actualBody=data.articles[bodyid]

        obj_indiv_headline_body= indiv_headline_body()
        obj_indiv_headline_body.body_id=bodyid
        obj_indiv_headline_body.headline=headline
        obj_indiv_headline_body.gold_stance = gold_stance_int
        obj_indiv_headline_body.body = actualBody
        obj_indiv_headline_body.unique_tuple_id=tuple_counter


        tuple_counter=tuple_counter+1



        data_my_format.append(obj_indiv_headline_body)



    return data_my_format


def convert_FNC_data_to_my_format(stances, data):
    #create a datasstructure of [headline, body, label]- matrix/2d array of strings.
    #Eg:
    #this guy related_rows will contain a list of headline_body_label_post_phase1_rows=[]
    #each headline_body_label_post_phase1_rows=[] will be an array of strings
    # [headline1, body1, stance1]
    # [headline2, body2, stance2]
    # [headline3, body3, stance3]

    related_matrix=[]

    #for each line separate out the headline ,bodyid, body and stance
    #they probably have it in the same format, but this is makes my life easier if i have it in my format.
    for s in stances:
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


def gen_or_load_feats(feat_fn, headlines, bodies, feature_file):
    if not os.path.isfile(feature_file):
        feats = feat_fn(headlines, bodies)
        np.save(feature_file, feats)

    return np.load(feature_file)


def gen_feats_as_numpy_feats(feat_fn, headlines, bodies):
    print("inside gen_feats_as_numpy_feats")
    feats = feat_fn(headlines, bodies)
    print("number of features is"+str(str(feats.shape)))
    np_feats=np.asarray(feats)
    return np_feats

def gen_or_load_feats_uofa(feat_fn, headlines, bodies, feature_file):
    if not os.path.isfile(feature_file):
        feats = feat_fn(headlines, bodies)
        np.save(feature_file, feats)

    return np.load(feature_file)


def generate_features_testdata(stances,dataset,name,vectorizer_phase2):
    h, b, y = [],[],[]

    for stance in stances:
        y.append(LABELS.index(stance['Stance']))
        h.append(stance['Headline'])
        b.append(dataset.articles[stance['Body ID']])

    #X_overlap = gen_or_load_feats(word_overlap_features_mithun, h, b, "features/overlap."+name+".npy")
    # X_refuting = gen_or_load_feats(refuting_features, h, b, "features/refuting."+name+".npy")
    # X_polarity = gen_or_load_feats(polarity_features, h, b, "features/polarity."+name+".npy")
    # X_hand = gen_or_load_feats(hand_features, h, b, "features/hand."+name+".npy")
    # X_hedge = gen_or_load_feats(hedging_features, h, b, "features/hedge."+name+".npy")
    #X_tf = gen_feats_as_numpy_feats(tf_features, h, b)
    X_tf=tf_features_transform(h, b,vectorizer_phase2)
    print("inside generate_features_testdata of rows in corpus post vectorization is:" + str(X_tf.shape))
    #X_combined = np.c_[X_hand, X_polarity, X_refuting, X_overlap,X_hedge]
    #X_combined = np.c_[X_tf, X_overlap]
    #X = np.c_[X_tf]
    return X_tf,y
    #print("inside generate_features_uofa of rows in X_combined is:" + str(X_combined.shape))
    #return X_combined,y


def generate_features_uofa(stances,dataset,name,vectorizer_phase2):
    h, b, y = [],[],[]

    for stance in stances:
        y.append(LABELS.index(stance['Stance']))
        h.append(stance['Headline'])
        b.append(dataset.articles[stance['Body ID']])

    X_overlap = gen_or_load_feats(word_overlap_features_mithun, h, b, "features/overlap." + name + ".npy")
    # X_refuting = gen_or_load_feats(refuting_features, h, b, "features/refuting."+name+".npy")
    # X_polarity = gen_or_load_feats(polarity_features, h, b, "features/polarity."+name+".npy")
    # X_hand = gen_or_load_feats(hand_features, h, b, "features/hand."+name+".npy")
    # X_hedge = gen_or_load_feats(hedging_features, h, b, "features/hedge."+name+".npy")
    #X_tf = gen_feats_as_numpy_feats(tf_features, h, b)
    X_tf=tf_features(h, b,vectorizer_phase2)
    print("inside generate_features_uofa of rows in corpus post vectorization is:" + str(X_tf.shape))
    #X_combined = np.c_[X_hand, X_polarity, X_refuting, X_overlap,X_hedge]
    #X_combined = np.c_[X_tf, X_overlap]
    #X = np.c_[X_tf]
    return X_tf,y
    #print("inside generate_features_uofa of rows in X_combined is:" + str(X_combined.shape))
    #return X_combined,y

def clean(s):
    # Cleans a string: Lowercasing, trimming, removing non-alphanumeric

    return " ".join(re.findall(r'\w+', s, flags=re.UNICODE)).lower()


def phase2_training(data,vectorizer_phase2):
    print("inside phase2_training_tf")
    entire_corpus=[]
    labels = np.array([[]])

    word_overlap_vector = np.empty((0, 1), float)
    hedging_words_vector = np.empty((0, 30), int)
    refuting_value_matrix= np.empty((0, 16), int)

    for obj_indiv_headline_body in data:

        gold_stance = obj_indiv_headline_body.gold_stance
        headline = obj_indiv_headline_body.headline
        actualBody = obj_indiv_headline_body.body

        headline_body_str = ""
        headline_body_str = headline_body_str + headline + "." + actualBody
        entire_corpus.append(headline_body_str)


        word_overlap = word_overlap_features_mithun(headline, actualBody)
        word_overlap_array = np.array([word_overlap])
        word_overlap_vector = np.vstack([word_overlap_vector, word_overlap_array])


        hedge_value = hedging_features_mithun(headline, actualBody)
        hedge_value_array = np.array([hedge_value])
        hedging_words_vector = np.vstack([hedging_words_vector, hedge_value_array])


        refuting_value = refuting_features_mithun(headline, actualBody)
        refuting_value_array = np.array([refuting_value])
        refuting_value_matrix = np.vstack([refuting_value_matrix, refuting_value_array])


        if (gold_stance == 0):
            labels = np.append(labels, 0)
        else:
            if (gold_stance == 1):
                labels = np.append(labels, 1)
            else:
                if(gold_stance==2):
                    labels = np.append(labels, 2)

    print("size of entire_corpus is:" + str(len(entire_corpus)))
    print("going to vectorize teh related corpus :" )

    tf_vector = vectorizer_phase2.fit_transform(entire_corpus)
    features=vectorizer_phase2.get_feature_names()
    writeToOutputFile("\n"+str(features),"featureNames_tfidf_vectorizer")

    print("number of rows in label list is is:" + str(len(labels)))
    print("going to feed this vectorized tf to a classifier:" )

    print("shape of corpus post vectorization is:" + str(tf_vector.shape))
    #print(tf_vector)
    #tf_vector_np=np.asarray(tf_vector)
    #print("shape of corpus post vectorization is:" + str(tf_vector_np.shape))
    #print(tf_vector_np)

    #print("number of rows in word_overlap_vector is:" + str(len(word_overlap_vector)))
    #print("shape of  word_overlap_vector is:" + str(word_overlap_vector.shape))

    #print("shape of  hedging_words_vector is:" + str(hedging_words_vector.shape))

    combined_vector =  scipy.sparse.hstack([tf_vector, word_overlap_vector,hedging_words_vector,refuting_value_matrix])
    #print("shape of combined_vector is:" + str(combined_vector.shape))


    #print(str(labels))
    #print("shape of labels is:" + str(labels.shape))


    #feed the vectors to an an svm, with labels.
    clf = svm.SVC(kernel='linear', C=1.0)
    #feature_vector=feature_vector.reshape(-1, 1)
    clf.fit(combined_vector, labels.ravel())
    #print("done training svm:" )

    return clf,vectorizer_phase2


def phase2_training_hollywood(data,vectorizer_phase2):
    #print("inside phase2_training_tf")
    entire_corpus=[]
    labels = np.array([[]])

    word_overlap_vector = np.empty((0, 1), float)
    hedging_words_vector = np.empty((0, 30), int)
    refuting_value_matrix= np.empty((0, 16), int)

    # hollywood_value_matrix = np.empty((0, 39), int)
    # terrorism_value_matrix = np.empty((0, 81), int)
    # health_value_matrix = np.empty((0, 38), int)
    # religion_value_matrix = np.empty((0, 14), int)
    # politics_value_matrix = np.empty((0, 36), int)

    for obj_indiv_headline_body in data:

        gold_stance = obj_indiv_headline_body.gold_stance
        headline = obj_indiv_headline_body.headline
        actualBody = obj_indiv_headline_body.body

        headline_body_str = ""
        headline_body_str = headline_body_str + headline + "." + actualBody
        entire_corpus.append(headline_body_str)


        word_overlap = word_overlap_features_mithun(headline, actualBody)
        word_overlap_array = np.array([word_overlap])
        word_overlap_vector = np.vstack([word_overlap_vector, word_overlap_array])


        hedge_value = hedging_features_mithun(headline, actualBody)
        hedge_value_array = np.array([hedge_value])
        hedging_words_vector = np.vstack([hedging_words_vector, hedge_value_array])


        refuting_value = refuting_features_mithun(headline, actualBody)
        refuting_value_array = np.array([refuting_value])
        refuting_value_matrix = np.vstack([refuting_value_matrix, refuting_value_array])


        if (gold_stance == 0):
            labels = np.append(labels, 0)
        else:
            if (gold_stance == 1):
                labels = np.append(labels, 1)
            else:
                if(gold_stance==2):
                    labels = np.append(labels, 2)

    #print("size of entire_corpus is:" + str(len(entire_corpus)))
    #print("going to vectorize teh related corpus :" )

    tf_vector = vectorizer_phase2.fit_transform(entire_corpus)
    features=vectorizer_phase2.get_feature_names()
    writeToOutputFile("\n"+str(features),"featureNames_tfidf_vectorizer")

    #print("number of rows in label list is is:" + str(len(labels)))
   # print("going to feed this vectorized tf to a classifier:" )

    #print("shape of corpus post vectorization is:" + str(tf_vector.shape))
    #print(tf_vector)
    #tf_vector_np=np.asarray(tf_vector)
    #print("shape of corpus post vectorization is:" + str(tf_vector_np.shape))
    #print(tf_vector_np)

    #print("number of rows in word_overlap_vector is:" + str(len(word_overlap_vector)))
    #print("shape of  word_overlap_vector is:" + str(word_overlap_vector.shape))

    #print("shape of  hedging_words_vector is:" + str(hedging_words_vector.shape))

<<<<<<< HEAD
    combined_vector =  scipy.sparse.hstack([tf_vector, word_overlap_vector,hedging_words_vector,refuting_value_matrix,
                                            hollywood_value_matrix,terrorism_value_matrix,health_value_matrix,
                                            religion_value_matrix,politics_value_matrix])
    #print("shape of combined_vector is:" + str(combined_vector.shape))
=======
    combined_vector =  scipy.sparse.hstack([tf_vector, word_overlap_vector,hedging_words_vector,refuting_value_matrix])
    print("shape of combined_vector is:" + str(combined_vector.shape))
>>>>>>> 69752814f6cdd8d91537710fdf983881eab135ee


    #print(str(labels))
    #print("shape of labels is:" + str(labels.shape))


    #feed the vectors to an an svm, with labels.
    clf = svm.SVC(kernel='linear', C=1.0)
    #feature_vector=feature_vector.reshape(-1, 1)
    clf.fit(combined_vector, labels.ravel())
    #print("done training svm:" )

    return clf,vectorizer_phase2


def phase2_training_with_lstm(data,vectorizer_phase2):
    #print("inside phase2_training_tf")
    entire_corpus=[]
    labels = np.array([[]])
    #no_of_unrelated=0
    #feature_vector= np.array([[]])
    # feature_vector=feature_vector.reshape(-1, 1)
    # labels = np.array([[]])

    #word_overlap_vector = np.array([])
    word_overlap_vector = np.empty((0, 1), float)
    hedging_words_vector = np.empty((0, 30), int)
    #lstm_features_matrix = np.empty((0, 4), float)
    refuting_value_matrix= np.empty((0, 16), int)

    for obj_indiv_headline_body in data:

        gold_stance = obj_indiv_headline_body.gold_stance
        headline = obj_indiv_headline_body.headline
        actualBody = obj_indiv_headline_body.body

        headline_body_str = ""
        headline_body_str = headline_body_str + headline + "." + actualBody
        entire_corpus.append(headline_body_str)




        word_overlap = word_overlap_features_mithun(headline, actualBody)
        word_overlap_array = np.array([word_overlap])
        word_overlap_vector = np.vstack([word_overlap_vector, word_overlap_array])


        hedge_value = hedging_features_mithun(headline, actualBody)
        hedge_value_array = np.array([hedge_value])
        hedging_words_vector = np.vstack([hedging_words_vector, hedge_value_array])

        #lstm_features_array = np.array([obj_indiv_headline_body.agree_lstm, obj_indiv_headline_body.disagree_lstm,
         #                               obj_indiv_headline_body.discuss_lstm, obj_indiv_headline_body.unrelated_lstm])
        #lstm_features_matrix = np.vstack([lstm_features_matrix, lstm_features_array])

        refuting_value = refuting_features_mithun(headline, actualBody)
        refuting_value_array = np.array([refuting_value])
        refuting_value_matrix = np.vstack([refuting_value_matrix, refuting_value_array])



        #print("gold_stance:"+str(gold_stance))
       # print(str(lstm_features_array))


        #stance= tuple[2]
       # print(stance)
        #agree:0
        #disagree:1
        #discuss:2
        #unrelated:3
        #lets call agrees as label 1 and disagrees as label 2
        if (gold_stance == 0):
            labels = np.append(labels, 0)
        else:
            if (gold_stance == 1):
                labels = np.append(labels, 1)
            else:
                if(gold_stance==2):
                    labels = np.append(labels, 2)

    #print("shape of  lstm_features_matrix is:" + str(lstm_features_matrix.shape))
    #print("shape of  lstm_features_matrix is:" + str(lstm_features_matrix))

    #sys.exit(1)

    #print("size of entire_corpus is:" + str(len(entire_corpus)))
    #print("going to vectorize teh related corpus :" )

    tf_vector = vectorizer_phase2.fit_transform(entire_corpus)
    features=vectorizer_phase2.get_feature_names()
    writeToOutputFile("\n"+str(features),"featureNames_tfidf_vectorizer")

    #print("number of rows in label list is is:" + str(len(labels)))
    #print("going to feed this vectorized tf to a classifier:" )

    #print("shape of corpus post vectorization is:" + str(tf_vector.shape))
    #print(tf_vector)
    #tf_vector_np=np.asarray(tf_vector)
    #print("shape of corpus post vectorization is:" + str(tf_vector_np.shape))
    #print(tf_vector_np)

    #print("number of rows in word_overlap_vector is:" + str(len(word_overlap_vector)))
    #print("shape of  word_overlap_vector is:" + str(word_overlap_vector.shape))

    #p rint("shape of  hedging_words_vector is:" + str(hedging_words_vector.shape))

    combined_vector =  scipy.sparse.hstack([tf_vector, word_overlap_vector,hedging_words_vector,lstm_features_matrix,refuting_value_matrix])
    #print("shape of combined_vector is:" + str(combined_vector.shape))


    #print(str(labels))
    #print("shape of labels is:" + str(labels.shape))


    #feed the vectors to an an svm, with labels.
    clf = svm.SVC(kernel='linear', C=1.0)
    #feature_vector=feature_vector.reshape(-1, 1)
    clf.fit(combined_vector, labels.ravel())
    #print("done training svm:" )

    return clf,vectorizer_phase2


def word_overlap_features_mithun(headline, body):

    clean_headline=doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)
    features = [
        len(set(clean_headline).intersection(clean_body)) / float(len(set(clean_headline).union(clean_body)))]

    return features

def hedging_features_mithun(headline, body):



    hedging_words = [
        'allegedly',
        'reportedli',
      'argue',
      'argument',
      'believe',
      'belief',
      'conjecture',
      'consider',
      'hint',
      'hypothesis',
      'hypotheses',
      'hypothesize',
      'implication',
      'imply',
      'indicate',
      'predict',
      'prediction',
      'previous',
      'previously',
      'proposal',
      'propose',
      'question',
      'speculate',
      'speculation',
      'suggest',
      'suspect',
      'theorize',
      'theory',
      'think',
      'whether'
    ]

    length_hedge=len(hedging_words)
    #print(length_hedge)
    hedging_body_vector = [0] * length_hedge


    #print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    #print(hedging_body_vector)

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)

    for word in clean_body:
        if word in hedging_words:
            index=hedging_words.index(word)
            #print(index)
            hedging_body_vector[index]=1

    #print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    #print(hedging_body_vector)
    return hedging_body_vector

def refuting_features_mithun(headline, body):

    refuting_words = [
        'fake',
        'fraud',
        'hoax',
        'false',
        'deny',
        'denies',
        'refute',
        'not',
        'despite',
        'nope',
        'doubt',
        'doubts',
        'bogus',
        'debunk',
        'pranks',
        'retract'
    ]

    length_hedge=len(refuting_words)
    refuting_body_vector = [0] * length_hedge

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)

    for word in clean_body:
        if word in refuting_words:
            index=refuting_words.index(word)
            #print(index)
            refuting_body_vector[index]=1


    return refuting_body_vector


def lstm_features(obj_data):

    length_hedge=len(hedging_words)
    #print(length_hedge)
    hedging_body_vector = [0] * length_hedge


    #print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    #print(hedging_body_vector)

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)

    for word in clean_body:
        if word in hedging_words:
            index=hedging_words.index(word)
            #print(index)
            hedging_body_vector[index]=1

    #print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    #print(hedging_body_vector)
    return hedging_body_vector

def tf_features(headlines, bodies,vectorizer_phase2):


    print("tf_features")
    entire_corpus=[]

    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        clean_headline = clean(headline)
        clean_body = clean(body)
        #clean_headline = get_tokenized_lemmas(clean_headline)
        #clean_body = get_tokenized_lemmas(clean_body)
        headline_body_str = ""
        headline_body_str = str(clean_headline)+"." + str(clean_body)
        entire_corpus.append(headline_body_str)

    #print("size of entire_corpus is:" + str(len(entire_corpus)))
    #print("going to vectorize teh related corpus :" )


    tf_vector_fit = vectorizer_phase2.fit(entire_corpus)
    tf_vector = vectorizer_phase2.transform(entire_corpus)
    features=vectorizer_phase2.get_feature_names()
    #writeToOutputFile("\n"+str(features),"featureNames_tfidf_vectorizer")

    #testing using a count vectorizer to make sure what am donig is currect
    # objCountVectorizer =createCountVectorizer()
    # tf_vector = objCountVectorizer.fit_transform(entire_corpus)
    # features=objCountVectorizer.get_feature_names()
    # writeToOutputFile("\n"+str(features),"featureNames_count_vectorizer")




    #

    #print(tf_vector .toarray())

    #tf_vector = vectorizer_phase2.calculate_tf_idf(entire_corpus)
     #X = vectorizer.fit_transform(document)
    #print(tf_vector)
   # print("number of rows in corpus post vectorization is:" + str(tf_vector.shape))
    return tf_vector

def tf_features_transform(headlines, bodies,vectorizer_phase2):


    #print("tf_features")
    entire_corpus=[]

    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        clean_headline = clean(headline)
        clean_body = clean(body)
        #clean_headline = get_tokenized_lemmas(clean_headline)
        #clean_body = get_tokenized_lemmas(clean_body)
        headline_body_str = ""
        headline_body_str = str(clean_headline)+"." + str(clean_body)
        entire_corpus.append(headline_body_str)

    #print("size of entire_corpus is:" + str(len(entire_corpus)))
    #print("going to vectorize teh related corpus :" )


    #tf_vector_fit = vectorizer_phase2.fit(entire_corpus)
    tf_vector = vectorizer_phase2.transform(entire_corpus)
    features=vectorizer_phase2.get_feature_names()
    #writeToOutputFile("\n"+str(features),"featureNames_tfidf_vectorizer")

    #testing using a count vectorizer to make sure what am donig is currect
    # objCountVectorizer =createCountVectorizer()
    # tf_vector = objCountVectorizer.fit_transform(entire_corpus)
    # features=objCountVectorizer.get_feature_names()
    # writeToOutputFile("\n"+str(features),"featureNames_count_vectorizer")




    #

    #print(tf_vector .toarray())

    #tf_vector = vectorizer_phase2.calculate_tf_idf(entire_corpus)
     #X = vectorizer.fit_transform(document)
    #print(tf_vector)
   # print("number of rows in corpus post vectorization is:" + str(tf_vector.shape))
    return tf_vector



def train_svm(my_features,labels):
    # print("inside phase2_training_tf")
    # entire_corpus=[]
    # labels = np.array([[]])
    # #no_of_unrelated=0
    # #feature_vector= np.array([[]])
    # # feature_vector=feature_vector.reshape(-1, 1)
    # # labels = np.array([[]])
    #
    # #just try creating a tf vector for one headline body combination.
    # # [headline1, body1, stance1]
    #
    # for tuple in data:
    #     print(str(tuple))
    #     sys.exit(1)
    #     headline_body_str=""
    #     headline = tuple[0]
    #     headline_body_str=headline_body_str+headline+"."
    #     #bodyid  = tuple['Body ID']
    #     actualBody=tuple[1]
    #     headline_body_str=headline_body_str+actualBody
    #     entire_corpus.append(headline_body_str)
    #
    #     stance= tuple[2]
    #     #agree:0
    #     #disagree:1
    #     #discuss:2
    #     #unrelated:3
    #     #lets call agrees as label 1 and disagrees as label 2
    #     if (stance == "agree"):
    #         labels = np.append(labels, 0)
    #     else:
    #         if (stance == "disagree"):
    #             labels = np.append(labels, 1)
    #         else:
    #             if(stance=="discuss"):
    #                 labels = np.append(labels, 2)
    #
    #
    #
    #
    # # #debug code to test printing the frist headline-body combination
    # # for indivlines in entire_corpus:
    # #     print(indivlines)
    # #     sys.exit(1)
    # #
    #
    #
    # #entire_corpus= ['The the the arachno centric trump and so if first document.','This is the and the of second second document.','And the third one.','Is this the first document?',]
    # #entire_corpus= ['higher, highest, automatic, automotive, automation, auto.','auto-bahn, autorickshaw']
    # print("size of entire_corpus is:" + str(len(entire_corpus)))
    # print("going to vectorize teh related corpus :" )
    #
    # tf_vector = vectorizer_phase2.fit_transform(entire_corpus)
    # features=vectorizer_phase2.get_feature_names()
    # writeToOutputFile("\n"+str(features),"featureNames_tfidf_vectorizer")

    #testing using a count vectorizer to make sure what am donig is currect
    # objCountVectorizer =createCountVectorizer()
    # tf_vector = objCountVectorizer.fit_transform(entire_corpus)
    # features=objCountVectorizer.get_feature_names()
    # writeToOutputFile("\n"+str(features),"featureNames_count_vectorizer")




    #

    #print(tf_vector .toarray())
    #sys.exit(1)
    #tf_vector = vectorizer_phase2.calculate_tf_idf(entire_corpus)
     #X = vectorizer.fit_transform(document)
    #print(tf_vector)
    print("number of rows in corpus post vectorization is:" + str(my_features.shape))

    print("number of rows in label list is is:" + str(len(labels)))
    print("going to feed this vectorized tf to a classifier:" )



    #feed the vectors to an an svm, with labels.
    clf = svm.SVC(kernel='linear', C=1.0)
    #feature_vector=feature_vector.reshape(-1, 1)
    clf.fit(my_features, labels.ravel())
    print("done training svm:" )

    return clf,vectorizer_phase2


def test_phase2_using_svm(test_data, svm_phase2, vectorizer_phase2_trained):

    #print("\ninside test_phase2_using_svm" )

    list_gold_label=[]
    entire_corpus=[]



    value2_int =2
    value1_int =1
    value0_int =0
    value3_int =3




    gold_predicted_combined=[[],[]]

    #print("total number of rows in test_data:" +str(len(test_data)))


    gold_int=[]
    word_overlap_vector=[]

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

        # add other feature vectors
        word_overlap = word_overlap_features_mithun(headline, actualBody)
        word_overlap_vector.append(word_overlap)

        #acccording to FNC guys, this is the mapping of classes to labels
        #agree:0
        #disagree:1
        #discuss:2
        #unrelated:3

        if (stance == "disagree"):
            gold_int.append(value1_int)
        else:
            if (stance == "agree"):
                gold_int.append(value0_int)
            else:
                if(stance=="discuss"):
                    gold_int.append(value2_int)
                else:
                    gold_int.append(value3_int)





    #print("\ngoing to vectorize headline_body_str :" )
    #print("\ntotal number of rows in entire_corpus:" +str(len(entire_corpus)))

    #print("\ntotal number of rows in word_overlap_vector:" + str(len(word_overlap_vector)))


    tf_vector =  vectorizer_phase2_trained.transform(entire_corpus)
    #print(tf_vector)
    #print("number of rows in vectorized entire_corpus is:" + str(tf_vector.shape))
    #print("going to feed this vectorized tf to a classifier:" )

    combined_vector=tf_vector+word_overlap_vector

    #print("going to predict class")
    #give that vector to your svm for prediction.
    pred_class=svm_phase2.predict(combined_vector)
    #print("going to print pred_class")
    #print("number of rows in pred_classis:" + str(pred_class.shape))
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


    writeToOutputFile("\n","errorAnalysis.txt")
    #find the ones in which i made a mistake/the predicted and gold didnt match
    dataCounter=0
    for tuple in test_data:
        # headline = tuple[0]
        actualBody=tuple[1]
        stance= tuple[2]

        # predicted_int=[]
        # entire_corpus.append(headline_body_str)
        headline_body_str=""
        headline = tuple[0]
        headline_body_str=headline_body_str+headline
        #bodyid  = tuple['Body ID']
        actualBody=tuple[1]

        # if(dataCounter<100):
        #     if(pred_label_int[dataCounter]!=gold_int[dataCounter]):
        #         #write to file.
                 #appendToFile("\n errored document count:"+str(dataCounter),"errorAnalysis.txt")
        #         appendToFile("\npred_label:"+str(pred_label_int[dataCounter]),"errorAnalysis.txt")
        #         appendToFile("\n gold_int[dataCounter] :"+str(gold_int[dataCounter]),"errorAnalysis.txt")
        #         appendToFile("\n  headline:"+headline,"errorAnalysis.txt")
        #         appendToFile("\n  actualBody:"+actualBody,"errorAnalysis.txt")
        #         appendToFile("\n  ***************","errorAnalysis.txt")
        #     dataCounter=dataCounter+1


    print("total number of items in pred_label_int is:"+str(len(pred_label_int)))



    #print("going to find number of rows in gold_int:" )
    numrows = len(gold_int)    # 3 rows in your example
    #numcols = len(gold_int[0]) # 2 columns in your example
    #print("number of rows in gold_int:" + str(numrows))
    #print("number of columns in gold_int:" + str(numcols))
    #print(gold_int)

    return gold_int, pred_label_int

def test_phase2_tf_hollywood(test_data_related_only, svm_phase2, vectorizer_phase2_trained, entire_testing_data_converted):

    print("\ninside test_phase2_tf_hollywood" )
    list_obj_indiv_headline_body=[]
    list_gold_label=[]
    entire_corpus=[]



    value2_int =2
    value1_int =1
    value0_int =0
    value3_int =3

    #word_overlap_vector = []
    #zero rows 1 column
    word_overlap_vector = np.empty((0, 1), float)
    hedging_words_vector = np.empty((0, 30), int)
    lstm_features_matrix=np.empty((0, 4), float)
    refuting_value_matrix = np.empty((0, 16), int)

    # hollywood_value_matrix = np.empty((0, 39), int)
    # terrorism_value_matrix = np.empty((0, 81), int)
    # health_value_matrix = np.empty((0, 38), int)
    # religion_value_matrix = np.empty((0, 14), int)
    # politics_value_matrix = np.empty((0, 36), int)

    gold_predicted_combined=[[],[]]

    print("total number of rows in test_data_related_only:" + str(len(test_data_related_only)))

    gold_int=[]
    for obj_indiv_headline_body in test_data_related_only:

        gold_stance= obj_indiv_headline_body.gold_stance
        headline=obj_indiv_headline_body.headline
        actualBody=obj_indiv_headline_body.body

        headline_body_str = ""
        headline_body_str = headline_body_str + headline+"."+actualBody
        entire_corpus.append(headline_body_str)

        # add other feature vectors
        word_overlap = word_overlap_features_mithun(headline, actualBody)
        word_overlap_array = np.array([word_overlap])
        word_overlap_vector = np.vstack([word_overlap_vector, word_overlap_array])

        hedge_value = hedging_features_mithun(headline, actualBody)
        hedge_value_array = np.array([hedge_value])
        hedging_words_vector = np.vstack([hedging_words_vector, hedge_value_array])

        refuting_value = refuting_features_mithun(headline, actualBody)
        refuting_value_array = np.array([refuting_value])
        refuting_value_matrix = np.vstack([refuting_value_matrix, refuting_value_array])

        # hollywood_value = Hollywood_features(headline, actualBody)
        # hollywood_value_value_array = np.array([hollywood_value])
        # hollywood_value_matrix = np.vstack([hollywood_value_matrix, hollywood_value_value_array])
        #

        #
        # terrorism_value = Terrorism_features(headline, actualBody)
        # terrorism_value_value_array = np.array([terrorism_value])
        # terrorism_value_matrix = np.vstack([terrorism_value_matrix, terrorism_value_value_array])
        #
        # health_value = Health_features(headline, actualBody)
        # health_value_value_array = np.array([health_value])
        # health_value_matrix = np.vstack([health_value_matrix, health_value_value_array])
        #
        # religion_value = Religion_features(headline, actualBody)
        # religion_value_value_array = np.array([religion_value])
        # religion_value_matrix = np.vstack([religion_value_matrix, religion_value_value_array])
        #
        # politics_value = Politics_features(headline, actualBody)
        # politics_value_value_array = np.array([politics_value])
        # politics_value_matrix = np.vstack([politics_value_matrix, politics_value_value_array])

        gold_int.append(gold_stance)
        # if (gold_stance == 0):
        #     gold_int.append(value1_int)
        # else:
        #     if (gold_stance == "agree"):
        #         gold_int.append(value0_int)
        #     else:
        #         if(gold_stance=="discuss"):
        #             gold_int.append(value2_int)
        #         else:
        #             gold_int.append(value3_int)





    #print("\ngoing to vectorize headline_body_str :" )
    #print("\ntotal number of rows in entire_corpus:" +str(len(entire_corpus)))





    tf_vector =  vectorizer_phase2_trained.transform(entire_corpus)
    #print(tf_vector)
    #print("number of rows in vectorized entire_corpus is:" + str(tf_vector.shape))
    #print("going to feed this vectorized tf to a classifier:" )

    #add the word overlap features
    #combined_vector = tf_vector + word_overlap_vector

    #combined_vector=np.concatenate(tf_vector,word_overlap_vector)
    #print("shape of  word_overlap_vector is:" + str(word_overlap_vector.shape))
    #print("shape of  lstm_features_matrix is:" + str(lstm_features_matrix.shape))
    #print("actual  lstm_features_matrix is:" + str(lstm_features_matrix))
    #print("lstm_features_matrix.dtype=" + str(lstm_features_matrix.dtype))

    #print("refuting_value_matrix.dtype=" + str(refuting_value_matrix.dtype))

    #print("refuting_value_matrix is =" + str(refuting_value_matrix))


    flstm_features_matrix=lstm_features_matrix.astype(float)
    #int_refuting_value_matrix = refuting_value_matrix.astype(float)
    #combined_vector = scipy.sparse.hstack([tf_vector, word_overlap_vector, hedging_words_vector, flstm_features_matrix])


   # combined_vector = scipy.sparse.hstack([tf_vector, word_overlap_vector, hedging_words_vector, refuting_value_matrix])
    combined_vector = scipy.sparse.hstack([tf_vector, word_overlap_vector, hedging_words_vector, refuting_value_matrix])

    # sparse.hstack(X, A.astype(float))

    #print("shape of combined_vector is:" + str(combined_vector.shape))
    # print("shape of  lstm_features_matrix is:" + str(flstm_features_matrix.shape))
    # print("actual  lstm_features_matrix is:" + str(flstm_features_matrix))
    # print("lstm_features_matrix.dtype=" + str(flstm_features_matrix.dtype))


    #print("going to predict class")
    #give that vector to your svm for prediction.
    pred_class=svm_phase2.predict(combined_vector)
    #print("going to print pred_class")
    #print("number of rows in pred_classis:" + str(pred_class.shape))
    #print(pred_class)


    #convert the predicted label to a regular list from numpy matrix

    pred_label_int=[]
    predicted_data=[]
    value2_float =2.0
    value1_float =1.0
    value0_float =0.0

    tuple_counter=0


    for obj_indiv_headline_body,x,entire_testing_data in itertools.zip_longest (test_data_related_only, np.nditer(pred_class),entire_testing_data_converted):


        #add the predicted label to the corresponding data structure value

        #obj_indiv_headline_body = test_data_related_only[tuple_counter]

        if(x==value2_float):
            pred_label_int.append(2)
            obj_indiv_headline_body.predicted_stance = 2
            entire_testing_data.predicted_stance = 2

        else:
            if(x==value1_float):
                pred_label_int.append(1)
                obj_indiv_headline_body.predicted_stance = 1
                entire_testing_data.predicted_stance = 1
            else:
                if(x==value0_float):
                    pred_label_int.append(0)
                    obj_indiv_headline_body.predicted_stance = 0
                    entire_testing_data.predicted_stance = 0

        tuple_counter = tuple_counter + 1
        predicted_data.append(obj_indiv_headline_body)


    writeToOutputFile("\n","errorAnalysis.txt")


    print("total number of items in pred_label_int is:"+str(len(pred_label_int)))



    #print("going to find number of rows in gold_int:" )
    numrows = len(gold_int)    # 3 rows in your example
    #numcols = len(gold_int[0]) # 2 columns in your example
    #print("number of rows in gold_int:" + str(numrows))
    #print("number of columns in gold_int:" + str(numcols))
    #print(gold_int)
    #print("number of rows in predicted_data:" + str(len(predicted_data)))

    return gold_int, pred_label_int,predicted_data,entire_testing_data_converted

def sendEmail(nameOfRun,toaddr):
    #gmailUsername="nn7607"
    gmailUsername="mithunpaul08"

    gmailPwd="Alohomora123+"
    #fromaddr="nn7607@gmail.com"
    fromaddr="mithunpaul08@gmail.com"
    #toaddr="mithunpaul08@gmail.com"
    #toaddr="mithunpaul@email.arizona.edu"
    subjectForEmail= nameOfRun+":Code finished running"
    carbonCopy = "mithunpaul@email.arizona.edu"
    #if on laptop dont switch path. This is required because cron runs as a separate process in a separate directory in chung
    #turn this to true, if pushing to run on chung.cs.arizona.edu
    isRunningOnServer=True;
    firstTimeRun=False;

    finalMessageToSend="hi, the code you were running is finished for"


    msg = "\r\n".join([
        "From: "+fromaddr,
        "To: " + toaddr,
        "CC: " + carbonCopy,
        "Subject:"+subjectForEmail,
        "",
        finalMessageToSend
    ])

    #print("getting here at 3687")
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    #print("getting here at 8637")
    server.starttls()
    #print("getting here at 52895")
    server.login(gmailUsername, gmailPwd)
    #print("getting here at 5498")
    server.sendmail(fromaddr, toaddr, msg)
    #print("getting here at 68468")
    server.quit()
    print("done sending email to:"+toaddr)


def normalize_word(w):
    return _wnl.lemmatize(w).lower()


def get_tokenized_lemmas(s):
    return [normalize_word(t) for t in nltk.word_tokenize(s)]


def clean(s):
    # Cleans a string: Lowercasing, trimming, removing non-alphanumeric

    return " ".join(re.findall(r'\w+', s, flags=re.UNICODE)).lower()


def remove_stopwords(l):
    # Removes stopwords from a list of tokens
    return [w for w in l if w not in feature_extraction.text.ENGLISH_STOP_WORDS]


def gen_or_load_feats(feat_fn, headlines, bodies, feature_file):
    if not os.path.isfile(feature_file):
        feats = feat_fn(headlines, bodies)
        np.save(feature_file, feats)

    return np.load(feature_file)





def refuting_features(headlines, bodies):
    _refuting_words = [
        'fake',
        'fraud',
        'hoax',
        'false',
        'deny', 'denies',
        # 'refute',
        'not',
        'despite',
        'nope',
        'doubt', 'doubts',
        'bogus',
        'debunk',
        'pranks',
        'retract'
    ]
    X = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        clean_headline = clean(headline)
        clean_headline = get_tokenized_lemmas(clean_headline)
        features = [1 if word in clean_headline else 0 for word in _refuting_words]
        X.append(features)
    return X


def polarity_features(headlines, bodies):
    _refuting_words = [
        'fake',
        'fraud',
        'hoax',
        'false',
        'deny', 'denies',
        'not',
        'despite',
        'nope',
        'doubt', 'doubts',
        'bogus',
        'debunk',
        'pranks',
        'retract'
    ]

    def calculate_polarity(text):
        tokens = get_tokenized_lemmas(text)
        return sum([t in _refuting_words for t in tokens]) % 2
    X = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        clean_headline = clean(headline)
        clean_body = clean(body)
        features = []
        features.append(calculate_polarity(clean_headline))
        features.append(calculate_polarity(clean_body))
        X.append(features)
    return np.array(X)


def ngrams(input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i + n])
    return output


def chargrams(input, n):
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i + n])
    return output


def append_chargrams(features, text_headline, text_body, size):
    grams = [' '.join(x) for x in chargrams(" ".join(remove_stopwords(text_headline.split())), size)]
    grams_hits = 0
    grams_early_hits = 0
    grams_first_hits = 0
    for gram in grams:
        if gram in text_body:
            grams_hits += 1
        if gram in text_body[:255]:
            grams_early_hits += 1
        if gram in text_body[:100]:
            grams_first_hits += 1
    features.append(grams_hits)
    features.append(grams_early_hits)
    features.append(grams_first_hits)
    return features


def append_ngrams(features, text_headline, text_body, size):
    grams = [' '.join(x) for x in ngrams(text_headline, size)]
    grams_hits = 0
    grams_early_hits = 0
    for gram in grams:
        if gram in text_body:
            grams_hits += 1
        if gram in text_body[:255]:
            grams_early_hits += 1
    features.append(grams_hits)
    features.append(grams_early_hits)
    return features


def hand_features(headlines, bodies):

    def binary_co_occurence(headline, body):
        # Count how many times a token in the title
        # appears in the body text.
        bin_count = 0
        bin_count_early = 0
        for headline_token in clean(headline).split(" "):
            if headline_token in clean(body):
                bin_count += 1
            if headline_token in clean(body)[:255]:
                bin_count_early += 1
        return [bin_count, bin_count_early]

    def binary_co_occurence_stops(headline, body):
        # Count how many times a token in the title
        # appears in the body text. Stopwords in the title
        # are ignored.
        bin_count = 0
        bin_count_early = 0
        for headline_token in remove_stopwords(clean(headline).split(" ")):
            if headline_token in clean(body):
                bin_count += 1
                bin_count_early += 1
        return [bin_count, bin_count_early]

    def count_grams(headline, body):
        # Count how many times an n-gram of the title
        # appears in the entire body, and intro paragraph

        clean_body = clean(body)
        clean_headline = clean(headline)
        features = []
        features = append_chargrams(features, clean_headline, clean_body, 2)
        features = append_chargrams(features, clean_headline, clean_body, 8)
        features = append_chargrams(features, clean_headline, clean_body, 4)
        features = append_chargrams(features, clean_headline, clean_body, 16)
        features = append_ngrams(features, clean_headline, clean_body, 2)
        features = append_ngrams(features, clean_headline, clean_body, 3)
        features = append_ngrams(features, clean_headline, clean_body, 4)
        features = append_ngrams(features, clean_headline, clean_body, 5)
        features = append_ngrams(features, clean_headline, clean_body, 6)
        return features

    X = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        X.append(binary_co_occurence(headline, body)
                 + binary_co_occurence_stops(headline, body)
                 + count_grams(headline, body))


    return X



def normalize_word(w):
    return _wnl.lemmatize(w).lower()
    # return w


def get_tokenized_lemmas(s):
    return [normalize_word(t) for t in nltk.word_tokenize(s)]
    # return s


def clean(s):
    # Cleans a string: Lowercasing, trimming, removing non-alphanumeric

    return " ".join(re.findall(r'\w+', s, flags=re.UNICODE)).lower()


def remove_stopwords(l):
    # Removes stopwords from a list of tokens
    return [w for w in l if w not in feature_extraction.text.ENGLISH_STOP_WORDS]
    # return l


def gen_or_load_feats(feat_fn, headlines, bodies, feature_file):
    if not os.path.isfile(feature_file):
        feats = feat_fn(headlines, bodies)
        np.save(feature_file, feats)

    return np.load(feature_file)


################################################################################################
################################################################################################
###################### 8 CLASSES FOR DIFFERENT TYPES OF NEWSES
def Terrorism_features(headline, body):    ## Terrorism includes local crimes and gang crimes also.
    Relative_words1 = [
        'government','ISIS','president','election','terrorists','CBI','armed','bomb','bombed','leader','al-Qaeda','Islamic','War',
        'attack', 'gun','shots','police','authorities','reported','officials','militants', 'kidnapped','insurgents','Iraq', 'strikes',
        'soldiers','civilians','fighting','ceasefire','army','officer','killed','rebel','battles','forces','military','FBI','Syria',
        'killing', 'airstrikes','abducting','clashes','beheading','civil','bloodshed','rescue','mission','crime','security','protest',
        'brutal','dead','shot','security','troops','graves','suspects','victims','patrol','jihadists','fighters','intelligence',
        'prisoners','criminal','bloody','explosion','blast','muslim','Syria','violence','victims','territory','bombardment',
        'Border', 'Protection','Marine','strategy','Prison','weapons','shootouts','gunmen'
    ]
    Relative_words = [normalize_word(w1) for w1 in Relative_words1]
    length_Terror = len(Relative_words)
    Terror_body_vector = [0] * length_Terror

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)
    for word in clean_body:
        if word in Relative_words:
            index=Relative_words.index(word)
            #print(index)
            Terror_body_vector[index]+=1
    for word in clean_headline:
        if word in Relative_words:
           index = Relative_words.index(word)
           Terror_body_vector[index] += 1
    #print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    #print(hedging_body_vector)
    return Terror_body_vector

##################################################################################################
##################################################################################################

def Hollywood_features(headline, body):    ## Hollywood includes words related to movie, theater and sports
    Relative_words1 = [
        'movie','star','actor','actoress','director','film','role','play','performance','TV','Celebrity','Post','fans','theater',
        'social', 'media','screenplay', 'production','starred', 'show','Oscar','awards','Filming','dated','music','camera','playing',
        'episodes','television','playing','role','cast','acting','followers','Entertainment','upcoming','casting','biopic','Trailer'


    ]
    Relative_words = [normalize_word(w1) for w1 in Relative_words1]
    length_Holly = len(Relative_words)

    Holly_body_vector = [0] * length_Holly

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)
    for word in clean_body:
        if word in Relative_words:
            index = Relative_words.index(word)
            # print(index)
            Holly_body_vector[index] += 1
    for word in clean_headline:
        if word in Relative_words:
            index = Relative_words.index(word)
            Holly_body_vector[index] += 1
    # print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    # print(hedging_body_vector)
    return Holly_body_vector


##################################################################################################
##################################################################################################

def Health_features(headline, body):    ## Health includes health, epedemics, and other health related news..
    Relative_words1 = [
        'doctors','cancer','kidney','Ebola','Health','infection','vomiting', 'diarrhoea', 'bleeding','illnesses','malaria',
        'Fever', 'fractured','operation','disease','misdiagnosed','diagnosed','Ministry','DNA', 'tests','drugs','Medical',
        'treatment','treated','epidemic', 'disease', 'Medics','suffering','Clinic','Hospital','surgery','sick','symptoms',
        'patient','virus','cure','spread','spreading'
    ]
    Relative_words = [normalize_word(w1) for w1 in Relative_words1]
    length_Health = len(Relative_words)

    Health_body_vector = [0] * length_Health

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)
    for word in clean_body:
        if word in Relative_words:
            index = Relative_words.index(word)
            # print(index)
            Health_body_vector[index] += 1
    for word in clean_headline:
        if word in Relative_words:
            index = Relative_words.index(word)
            Health_body_vector[index] += 1
    # print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    # print(hedging_body_vector)
    return Health_body_vector

##################################################################################################
##################################################################################################

def Religion_features(headline, body):    ## Religion includes religion, culture. ## This also includes other remianing news.
    Relative_words1 = [
        'Christians','catholic','Church','Game','company','product','Olympic','Medal','sport','revenue','earnings','product',
        'launch','match'
    ]
    Relative_words = [normalize_word(w1) for w1 in Relative_words1]
    length_Religion = len(Relative_words)
    Religion_body_vector = [0] * length_Religion

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)
    for word in clean_body:
        if word in Relative_words:
            index = Relative_words.index(word)
            # print(index)
            Religion_body_vector[index] += 1
    for word in clean_headline:
        if word in Relative_words:
            index = Relative_words.index(word)
            Religion_body_vector[index] += 1
    # print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    # print(hedging_body_vector)
    return Religion_body_vector


##################################################################################################
##################################################################################################
def Politics_features(headline, body):    ## Hollywood includes words related to movie, theater and sports
    Relative_words1 = [
        'role','play','leader','countries','political','economic','spokesman','justice','Foreign', 'Secretary','alliance', 'presidency',
        'Duties','House','violence','spokesman','officials','Ministry','State','Defense','Council','member', 'Congress','Department',
        'plan','international','journalist','Republican', 'lawmakers','policies','Development','Minister','Public','deputy','legislators',
        'politician'

    ]
    Relative_words = [normalize_word(w1) for w1 in Relative_words1]
    length_Politics = len(Relative_words)
    Politics_body_vector = [0] * length_Politics

    clean_headline = doAllWordProcessing(headline)
    clean_body = doAllWordProcessing(body)
    for word in clean_body:
        if word in Relative_words:
            index = Relative_words.index(word)
            # print(index)
            Politics_body_vector[index] += 1
    for word in clean_headline:
        if word in Relative_words:
            index = Relative_words.index(word)
            Politics_body_vector[index] += 1
    # print("shape of hedging_body_vector is" + str(len(hedging_body_vector)))
    # print(hedging_body_vector)
    return Politics_body_vector

##################################################################################################
##################################################################################################
