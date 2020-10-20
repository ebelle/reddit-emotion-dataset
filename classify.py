import json
import argparse

from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
    TfidfVectorizer,
)
from sklearn.feature_extraction import DictVectorizer

from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn import metrics

from utils import load_data, clean_text, make_split
from feature_extractors import (
    Tokenize,
    ExtractPOS,
    SlidingWindow,
    EmpathFeatures,
    VaderFeatures,
)


def main(args):

    print("Loading dataset.")
    df = load_data(args.filename)

    df["text"] = df["text"].apply(clean_text)


    train, test = make_split(df)

    # optionally add features to pipeline
    transformer_list = []

    if args.unigrams:
        transformer_list.append(
            (
                "unigrams",
                Pipeline(
                    [("vect", CountVectorizer(ngram_range=(1, 1), max_df=args.max_df)),]
                ),
            )
        )
    if args.bigrams:
        transformer_list.append(
            (
                "bigrams",
                Pipeline(
                    [("vect", CountVectorizer(ngram_range=(1, 2), max_df=args.max_df)),]
                ),
            )
        )
    if args.trigrams:
        transformer_list.append(
            (
                "trigrams",
                Pipeline(
                    [("vect", CountVectorizer(ngram_range=(1, 3), max_df=args.max_df)),]
                ),
            )
        )
    if args.part_of_speech:
        transformer_list.append(
            (
                "part_of_speech",
                Pipeline(
                    [
                        ("parts_speech", ExtractPOS()),
                        ("vect", CountVectorizer(analyzer="word")),
                    ]
                ),
            )
        )
    if args.empath:
        transformer_list.append(
            (
                "empath_features",
                Pipeline(
                    [
                        ("token", Tokenize()),
                        ("empath", EmpathFeatures()),
                        ("vect", DictVectorizer()),
                    ]
                ),
            )
        )
    if args.vader:
        transformer_list.append(
            (
                "vader_features",
                Pipeline([("vader", VaderFeatures()), ("vect", DictVectorizer()),]),
            )
        )
    if args.tfidf:
        transformer_list.append(
            (
                "tfidf_features",
                Pipeline(
                    [
                        ("vect", CountVectorizer(ngram_range=(1, 2), max_df=0.5)),
                        ("tfidf", TfidfTransformer()),
                    ]
                ),
            )
        )
    if args.char_features:
        transformer_list.append(
            (
                "char_features",
                Pipeline(
                    [("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 6))),]
                ),
            )
        )
    if args.sliding_window:
        transformer_list.append(
            (
                "sliding_window",
                Pipeline([("pos", SlidingWindow()), 
                ("vect", DictVectorizer()),]))
        )
    # choose classifier
    classifier_dict = {
        "sgd": ("sgd", SGDClassifier()),
        "svc": ("svc", SVC(gamma="scale")),
        "multinomial_nb": ("mnb", MultinomialNB()),
        "random_forest": ("rf", RandomForestClassifier()),
        "logistic_regression": ("lr", LogisticRegression(solver="sag")),
    }
    classifier = classifier_dict[args.classifier]

    model = Pipeline(
        [("features", FeatureUnion(transformer_list=transformer_list)), classifier]
    )
    
    print(model)
    print("writing to pipeline")
    model.fit(train["text"], train["emotions"])

    print("predicting")
    y = model.predict(test["text"])
    print(metrics.classification_report(y, test["emotions"], digits=6))
    print(metrics.confusion_matrix(y, test["emotions"]))
    print(metrics.accuracy_score(y, test["emotions"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="json file where reddit comments are stored")
    parser.add_argument(
        "--max-df",
        default=0.5,
        type=float,
        help="When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words).",
    )
    parser.add_argument("--unigrams", default=False, action="store_true")
    parser.add_argument("--bigrams", default=False, action="store_true")
    parser.add_argument("--trigrams", default=False, action="store_true")
    parser.add_argument("--part-of-speech", default=False, action="store_true")
    parser.add_argument("--vader", default=False, action="store_true")
    parser.add_argument("--empath", default=False, action="store_true")
    parser.add_argument("--tfidf", default=False, action="store_true")
    parser.add_argument("--char-features", default=False, action="store_true")
    parser.add_argument("--sliding-window", default=False, action="store_true")
    parser.add_argument(
        "--classifier",
        default="sgd",
        type=str,
        choices=[
            "sgd",
            "svc",
            "multinomial_nb",
            "random_forest",
            "logistic_regression",
        ],
    )

    main(parser.parse_args())
