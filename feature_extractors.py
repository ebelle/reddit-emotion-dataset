from tqdm import tqdm
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from empath import Empath
from sklearn.base import BaseEstimator, TransformerMixin


class Tokenize(BaseEstimator,TransformerMixin):

    def __init__(self, strip=True):
        self.strip = strip

    def fit(self,x,y=None):
        return self 

    def transform(self,x):
        return [" ".join(self.tokenize(doc)) for doc in x]

    def tokenize(self, document):
        for sent in nltk.tokenize.sent_tokenize(document):
            for token in nltk.tokenize.wordpunct_tokenize(sent):
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token
                yield token


class ExtractPOS(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, comments):
        L = []
        print("Extracting POS.")
        for comment in tqdm(comments):
            comment = nltk.pos_tag(comment.split())
            comment = " ".join([x[1] for x in comment])
            L.append(comment)
        return L


class SlidingWindow(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, comments):
        L = []
        print("Extracting sliding window.")
        for sentence in tqdm(comments):
            feat_dict = {}
            sentence = sentence.split()
            len_sentence = len(sentence)
            pos_tags = nltk.pos_tag(sentence)
            tags = []
            for x in pos_tags:
                tags.append(x[0]+'_'+x[1])
            for i in range(len_sentence):
                # for the first word in the sentence, add sentence boundary as previous token
                if i == 0:
                    feat_dict["word-1"] = ("SB_#")
                    feat_dict["word"] = tags[i]
                    feat_dict["word+1"] = tags[i + 1]
                elif len_sentence - 1 > i > 0:
                    feat_dict["word-1"] = tags[i - 1]
                    feat_dict["word"] = tags[i]
                    feat_dict["word+1"] = tags[i + 1]
                # for the last word in the sentence, add sentence boundary as next token
                elif i == len_sentence:
                    feat_dict["word-1"] = tags[i - 1]
                    feat_dict["word-1"] = tags[i]
                    feat_dict["word+1"] = ("SB_#")
            L.append(feat_dict)
        return L


class EmpathFeatures(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.lexicon = Empath()

    def fit(self, x, y=None):
        return self

    def transform(self, comments):
        L = []
        print("Extracting Empath features.")
        for comment in tqdm(comments):
            feature_dict = self.lexicon.analyze(comment, normalize=True)
            L.append(feature_dict)
        return L


class VaderFeatures(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def fit(self, x, y=None):
        return self

    def transform(self, comments):
        L = []
        print("Extracting Vader features.")
        for comment in tqdm(comments):
            sid_dict = self.sid.polarity_scores(comment)
            L.append(sid_dict)
        return L
