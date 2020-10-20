import csv
from sklearn.model_selection import train_test_split
import pandas as pd
import json
from detectormorse import detector
import re
import string
from nltk.tokenize import TweetTokenizer
from keras.utils import to_categorical


def load_data(filename):
    with open(filename, "r") as source:
        data = json.load(source)
        df = pd.DataFrame(list(data.items()), columns=["text", "emotions"])
    return df


def make_split(df):
    train, test = train_test_split(df, test_size=0.2)
    return train, test


segment = detector.default_model().segments
tokenize = TweetTokenizer().tokenize


def clean_text(post):
    cleaned_sentences = []
    post = re.sub(r"http\S+", "", post)
    for sentence in segment(post):
        sentence = tokenize(sentence)
        sentence = [token.casefold() for token in sentence if token]
        cleaned_sentences.append(" ".join(sentence))
    cleaned_post = " ".join(cleaned_sentences)
    return cleaned_post
