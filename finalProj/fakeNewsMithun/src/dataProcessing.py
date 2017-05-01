from csv import DictReader
from sklearn.feature_extraction.text import TfidfTransformer


class ProcessData():
    def read(self,filename):
        rows = []
        with open(self.path + "/" + filename, "r", encoding='utf-8') as table:
            r = DictReader(table)

            for line in r:
                rows.append(line)
        return rows

    def calculate_tf_idf(counts):
        #transformer = TfidfTransformer(smooth_idf=False)
        transformer = TfidfTransformer(norm='l2', smooth_idf=False, sublinear_tf=False,
                 use_idf=True)
        tfidf = transformer.fit_transform(counts)
        tfidf.toarray()
