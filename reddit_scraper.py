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

    today = date.today()

    if not args.get_comments:
        for emotion, synonym_list in args.emotion_dict.items():
            # create dataframe to store comments
            topics_data = pd.DataFrame(
                {
                    "title": [],
                    "score": [],
                    "id": [],
                    "url": [],
                    "comms_num": [],
                    "created": [],
                    "emotion": []
                }
            )
            for synonym in synonym_list:
                topics_dict = {
                    "title": [],
                    "score": [],
                    "id": [],
                    "url": [],
                    "comms_num": [],
                    "created": [],
                    "emotion": []
                }
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
                            topics_dict["title"].append(emotional_submission.title)
                            topics_dict["score"].append(emotional_submission.score)
                            topics_dict["id"].append(emotional_submission.id)
                            topics_dict["url"].append(emotional_submission.url)
                            topics_dict["comms_num"].append(
                                emotional_submission.num_comments
                            )
                            topics_dict["created"].append(emotional_submission.created)
                            topics_dict["emotion"].append(emotion)
                # combine all the dictionaries into one dataframe
                topics_data = pd.concat([pd.DataFrame(topics_dict), topics_data])
        if args.titles_only:
            title_path = os.path.join(args.save_path,f'{today.strftime("%Y.%m.%d")}_titles.csv')
            topics_data.to_csv(title_path,index=False)
            quit()
    else:
        topics_data = pd.read_csv(args.get_comments)
    
    with open(os.path.join(args.save_path,f'{today.strftime("%Y.%m.%d")}_comments.json'), "w") as sink:
        comment_dict = {}
        for thread_id,emotion in zip(topics_data.id,topics_data.emotion):
            submission = reddit.submission(id=thread_id)
            for comment in submission.comments:
                # ignore “load more comments”
                if isinstance(comment, MoreComments):
                    continue
                # ignore “continue this thread” links and short comments
                if len(comment.body.split()) > 3:
                    comment_dict[comment.body] = emotion
        logging.info("%d %s comments scraped.", len(comment_dict), emotion)
        json.dump(comment_dict, sink)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-path", help="folder for saving scraped comments")
    parser.add_argument(
        "--reddit-credentials", help="yaml file containing reddit credentials",
    )
    parser.add_argument("--titles-only", default=False, action="store_true",help='if you would like to hand clean the titles')
    parser.add_argument("--get-comments", default=None, type=str,help='csv hand cleaned titles')
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
            "unreasonably"
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
