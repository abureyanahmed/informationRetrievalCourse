class indiv_headline_body(object):
    def __init__(self):
        self.headline = ""
        self.body = ""
        self.body_id = 0
        self.predicted_stance = 0
        self.gold_stance = 0
        self.confidence = 1
        self.unique_tuple_id=0
        self.agree_lstm=0.0000000001
        self.disagree_lstm = 0.0000000001
        self.discuss_lstm = 0.0000000001
        self.unrelated_lstm = 0.0000000001

