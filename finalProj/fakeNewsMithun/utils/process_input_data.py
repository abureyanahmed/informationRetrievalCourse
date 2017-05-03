from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from csv import DictReader
from sklearn.feature_extraction.text import TfidfTransformer

#
#
# def read(self,filename):
#     rows = []
#     with open(self.path + "/" + filename, "r", encoding='utf-8') as table:
#         r = DictReader(table)
#
#         for line in r:
#             rows.append(line)
#     return rows


def tokenize(document):
    vectorizer = CountVectorizer(min_df=1)
    # #corpus = ['This is the first document.','This is the second second document.','And the third one.',
    #           'Is this the first document?',]
    X = vectorizer.fit_transform(document)
    print(X.toarray())
    return X

def calculate_tf_idf(counts):
    print("getting inside calculate_tf_idf")
    transformer = TfidfTransformer(norm='l2', smooth_idf=False, sublinear_tf=False,
             use_idf=True)
    tfidf = transformer.fit_transform(counts)

    return tfidf

