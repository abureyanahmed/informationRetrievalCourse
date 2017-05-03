import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from csv import DictReader
from sklearn.feature_extraction.text import TfidfTransformer

nltk.download('punkt') # if necessary...


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

def tokenize(document):
    vectorizer = CountVectorizer(min_df=1)

    X = vectorizer.fit_transform(document)

    return X

def calculate_tf_idf(counts):
    print("getting inside calculate_tf_idf")
    transformer = TfidfTransformer(norm='l2', smooth_idf=False, sublinear_tf=False,
             use_idf=True)
    tfidf = transformer.fit_transform(counts)

    return tfidf

