from utils.fileWriter import appendToFile
from utils.process_input_data import cosine_sim


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

def calculateAccuracy(d,unrelated_threshold):
    TP=FP=FN=TN=0
    goldlabel=""

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


    precision=TP/(TP+FP)
    print("precision:"+precision)
    #recall=TP/(TP+FP)
    accuracy=correct_prediction/total_pairs
    return accuracy
