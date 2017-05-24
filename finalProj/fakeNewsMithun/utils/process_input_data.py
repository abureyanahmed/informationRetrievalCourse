from __future__ import division
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from csv import DictReader
from sklearn.feature_extraction.text import TfidfTransformer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


nltk.download("stopwords")

#nltk.download('punkt')
#nltk.download('wordnet')

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def my_lemmatize(doc):
    my_wnl = WordNetLemmatizer()
    lemmatized_version=[]


def doAllWordProcessing(doc):
    lemmatized_version=[]
    for t in word_tokenize(doc):
        if t not in stopwords.words('english'):
            t_lower=t.lower().translate(remove_punctuation_map)
            my_wnl = WordNetLemmatizer()
            lmv=my_wnl.lemmatize(t_lower)
            stemmed=stemmer.stem(lmv)
            #print(lmv)
            lemmatized_version.append(stemmed)
    return lemmatized_version

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def tokenize(document,vectorizer_phase2):
    #vectorizer = CountVectorizer(min_df=1)

    X = vectorizer.fit_transform(document)

    return X

def calculate_tf_idf(counts):
    print("getting inside calculate_tf_idf")
    transformer = TfidfTransformer(norm='l2', smooth_idf=False, sublinear_tf=False,
             use_idf=True)
    tfidf = transformer.fit_transform(counts)

    return tfidf

def createAtfidfVectorizer():
    #vectorizer2 = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    vectorizer2 = TfidfVectorizer(tokenizer=normalize,encoding=u'utf-8', decode_error=u'ignore',strip_accents='unicode',stop_words='english' )
    #vectorizer2 = TfidfVectorizer(tokenizer=normalize,encoding=u'utf-8', decode_error=u'ignore',strip_accents='unicode',stop_words='english' )
    return vectorizer2


def createCountVectorizer():
    cvectorizer = CountVectorizer(min_df=1)
    CountVectorizer(tokenizer=LemmaTokenizer())
    return cvectorizer
