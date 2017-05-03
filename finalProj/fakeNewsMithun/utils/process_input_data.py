from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer


def tokenize(document):
    vectorizer = CountVectorizer(min_df=1)
    # #corpus = ['This is the first document.','This is the second second document.','And the third one.',
    #           'Is this the first document?',]
    X = vectorizer.fit_transform(document)
    print(X.toarray())
    return X
