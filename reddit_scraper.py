import os
import logging
import pandas as pd
import praw
from praw.models import MoreComments
import yaml
import re
import json
from datetime import date
import argparse

logging.basicConfig(level="INFO", format="%(message)s")


def main(args):
    
    with open(args.reddit_credentials, "r") as source:
        credentials = yaml.safe_load(source)

    reddit = praw.Reddit(
        client_id=credentials["id"],
        client_secret=credentials["secret"],
        user_agent=credentials["agent"],
    )

    subreddit = reddit.subreddit(args.subreddit)
    
    if not os.path.exists(args.save_path):
        os.mkdir(args.save_path)

    with open(os.path.join(args.save_path, "comments.json"), "w") as sink:
        titles = []
        ids = []
        emotions = []
        for emotion, synonym_list in args.emotion_dict.items():
            # create dataframe to store comments
            for synonym in synonym_list:
                query = subreddit.search(synonym, limit=args.query_limit)
                for emotional_submission in query:
                    if synonym in emotional_submission.title:
                        # exclude submissions with unwanted words
                        if any(
                            word in emotional_submission.title
                            for word in args.excluded_words
                        ):
                            pass
                        else:
                            titles.append(emotional_submission.title)
                            ids.append(emotional_submission.id)
                            emotions.append(emotion)
            
            final_dict = {'comments': [],
            'comment_titles': [],
            'comment_emotions': []}
            for idx,t,e in zip(ids,titles,emotions):
                submission = reddit.submission(id=idx)
                for comment in submission.comments:
                    # ignore “load more comments”
                    if isinstance(comment, MoreComments):
                        continue
                    # ignore “continue this thread” links and short comments
                    if len(comment.body.split()) > 3:
                        final_dict['comments'].append(comment.body)
                        final_dict['comment_titles'].append(t)
                        final_dict['comment_emotions'].append(e)
            json.dump(final_dict, sink)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-path", help="folder for saving scraped comments")
    parser.add_argument(
        "--reddit-credentials", help="yaml file containing reddit credentials",
    )
    parser.add_argument(
        "--titles-only",
        default=False,
        action="store_true",
        help="if you would like to hand clean the titles",
    )
    parser.add_argument(
        "--get-comments", default=None, type=str, help="csv hand cleaned titles"
    )
    parser.add_argument(
        "--query-limit",
        default=500,
        type=int,
        help="maximum number of queries to reddit",
    )
    parser.add_argument(
        "--subreddit", default="askreddit", type=str, help="subreddit to scrape"
    )
    parser.add_argument(
        "--excluded-words",
        default=[
            "song",
            "songs",
            "film",
            "films",
            "movie",
            "movies",
            "joke",
            "jokes",
            "lyrics",
            "book",
            "books",
            "irrational",
            "unreasonably",
        ],
        type=list,
        help="list of words not wanted in the title of the submission",
    )
    parser.add_argument(
        "--emotion-dict",
        default={
            "happy": [
                "happy",
                "happier",
                "happiest",
                "ecstatic",
                "pleasure",
                "joy",
                "joyful",
                "joyous",
                "happiness",
            ],
            "surprised": [
                "surprised",
                "more surprised",
                "most surprised",
                "shocked",
                "most shocked",
                "surprise",
                "biggest surpise",
                "shock",
            ],
            "sad": [
                "sad",
                "sadder",
                "saddest",
                "depressed",
                "more depressed" "most depressed",
                "sadness",
                "depression",
            ],
            "angry": [
                "angry",
                "angrier",
                "angriest",
                "enraged",
                "pissed off",
                "piss you off",
                "anger",
                "rage",
            ],
            "afraid": [
                "afraid",
                "more afraid",
                "most afraid",
                "frightened",
                "fear",
                "creepy",
            ],
            "disgusted": [
                "disgusted",
                "more disgusted",
                "most disgusted",
                "grossed out",
                "most grossed out",
                "most appalled",
                "appalled",
                "disgust",
            ],
        },
        type=dict,
        help="dictionary of emotions and emotion synonyms to query reddit for",
    )

    main(parser.parse_args())
