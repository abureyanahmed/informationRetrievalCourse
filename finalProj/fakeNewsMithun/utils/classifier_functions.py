from __future__ import division
import os
import numpy as np
import smtplib
import sys
from sklearn import svm
import os
import re
import nltk
import numpy as np
from sklearn import feature_extraction
from tqdm import tqdm

from utils.fileWriter import writeToOutputFile
from utils.process_input_data import cosine_sim
from utils.feature_engineering import refuting_features, polarity_features, hand_features,hedging_features
from utils.feature_engineering import word_overlap_features
from tqdm import tqdm

from utils.process_input_data import createAtfidfVectorizer

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
            headline_body_label=[]
            headline_body_label.append(headline)
            headline_body_label.append(actualBody)
            headline_body_label.append(stance)
            related_matrix.append(headline_body_label)

        #append this headline_body_label guy to the big matrix


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

def convert_data_to_headline_body_stance_format(data):
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
        print(stance)

        headline_body_label=[]
        headline_body_label.append(headline)
        headline_body_label.append(actualBody)
        headline_body_label.append(stance)
        #append this headline_body_label guy to the big matrix
        related_matrix.append(headline_body_label)



    return related_matrix

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
        print(stance)

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




def generate_features_uofa(stances,dataset,name):
    h, b, y = [],[],[]

    for stance in stances:
        y.append(LABELS.index(stance['Stance']))
        h.append(stance['Headline'])
        b.append(dataset.articles[stance['Body ID']])

    #X_overlap = gen_or_load_feats(word_overlap_features, h, b, "features/overlap."+name+".npy")
    # X_refuting = gen_or_load_feats(refuting_features, h, b, "features/refuting."+name+".npy")
    # X_polarity = gen_or_load_feats(polarity_features, h, b, "features/polarity."+name+".npy")
    # X_hand = gen_or_load_feats(hand_features, h, b, "features/hand."+name+".npy")
    # X_hedge = gen_or_load_feats(hedging_features, h, b, "features/hedge."+name+".npy")
    #X_tf = gen_feats_as_numpy_feats(tf_features, h, b)
    X_tf=tf_features(h, b)
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


def phase2_training_tf(data,vectorizer_phase2):
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
        print(str(tuple))
        sys.exit(1)
        headline_body_str=""
        headline = tuple[0]
        headline_body_str=headline_body_str+headline+"."
        #bodyid  = tuple['Body ID']
        actualBody=tuple[1]
        headline_body_str=headline_body_str+actualBody
        entire_corpus.append(headline_body_str)

        stance= tuple[2]
        #agree:0
        #disagree:1
        #discuss:2
        #unrelated:3
        #lets call agrees as label 1 and disagrees as label 2
        if (stance == "agree"):
            labels = np.append(labels, 0)
        else:
            if (stance == "disagree"):
                labels = np.append(labels, 1)
            else:
                if(stance=="discuss"):
                    labels = np.append(labels, 2)




    # #debug code to test printing the frist headline-body combination
    # for indivlines in entire_corpus:
    #     print(indivlines)
    #     sys.exit(1)
    #


    #entire_corpus= ['The the the arachno centric trump and so if first document.','This is the and the of second second document.','And the third one.','Is this the first document?',]
    #entire_corpus= ['higher, highest, automatic, automotive, automation, auto.','auto-bahn, autorickshaw']
    print("size of entire_corpus is:" + str(len(entire_corpus)))
    print("going to vectorize teh related corpus :" )

    tf_vector = vectorizer_phase2.fit_transform(entire_corpus)
    features=vectorizer_phase2.get_feature_names()
    writeToOutputFile("\n"+str(features),"featureNames_tfidf_vectorizer")

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
    print("number of rows in corpus post vectorization is:" + str(tf_vector.shape))

    print("number of rows in label list is is:" + str(len(labels)))
    print("going to feed this vectorized tf to a classifier:" )



    #feed the vectors to an an svm, with labels.
    clf = svm.SVC(kernel='linear', C=1.0)
    #feature_vector=feature_vector.reshape(-1, 1)
    clf.fit(tf_vector, labels.ravel())
    print("done training svm:" )

    return clf,vectorizer_phase2

def word_overlap_features(headlines, bodies):
    X = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        clean_headline = clean(headline)
        clean_body = clean(body)
        clean_headline = get_tokenized_lemmas(clean_headline)
        clean_body = get_tokenized_lemmas(clean_body)
        features = [
            len(set(clean_headline).intersection(clean_body)) / float(len(set(clean_headline).union(clean_body)))]
        X.append(features)
    return X


def tf_features(headlines, bodies):


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

    vectorizer_phase2 = createAtfidfVectorizer()
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

    print("\ninside test_phase2_using_svm" )

    list_gold_label=[]
    entire_corpus=[]



    value2_int =2
    value1_int =1
    value0_int =0
    value3_int =3




    gold_predicted_combined=[[],[]]

    print("total number of rows in test_data:" +str(len(test_data)))


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





    print("\ngoing to vectorize headline_body_str :" )
    print("\ntotal number of rows in entire_corpus:" +str(len(entire_corpus)))



    tf_vector =  vectorizer_phase2_trained.transform(entire_corpus)
    #print(tf_vector)
    print("number of rows in vectorized entire_corpus is:" + str(tf_vector.shape))
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
    print("number of rows in gold_int:" + str(numrows))
    #print("number of columns in gold_int:" + str(numcols))
    #print(gold_int)

    return gold_int, pred_label_int


def sendEmail(nameOfRun,toaddr):
    #gmailUsername="nn7607"
    gmailUsername="mithunpaul08"

    gmailPwd="Alohomora456+"
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

import os
import re
import nltk
import numpy as np
from sklearn import feature_extraction
from tqdm import tqdm


_wnl = nltk.WordNetLemmatizer()


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




def word_overlap_features(headlines, bodies):
    X = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        clean_headline = clean(headline)
        clean_body = clean(body)
        clean_headline = get_tokenized_lemmas(clean_headline)
        clean_body = get_tokenized_lemmas(clean_body)
        features = [
            len(set(clean_headline).intersection(clean_body)) / float(len(set(clean_headline).union(clean_body)))]
        X.append(features)
    return X


def hedging_features(headlines, bodies):
    _hedging_words = [
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
    X = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        clean_headline = clean(headline)
        clean_headline = get_tokenized_lemmas(clean_headline)
        features = [1 if word in clean_headline else 0 for word in _hedging_words]
        X.append(features)
    return X

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
