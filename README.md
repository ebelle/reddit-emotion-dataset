# reddit-emotion-dataset
Creates a emotion dataset using responses to AskReddit questions such as "what makes you happy?"

To use the scraper, you need a yaml file with your reddit credentials. It can be run as:

bash
python reddit_scraper.py --save-path ../data/ \
--reddit-credentials credentials.yaml

Default search terms in the title are:
"happy":["happy","happier", "happiest", "ecstatic", "pleasure","joy", "joyful", "joyous","happiness"]
"surprised":["surprised", "more surprised", "most surprised", "shocked", "most shocked","surprise", "biggest surpise", "shock"]
"sad": ["sad", "sadder", "saddest", "depressed", "more depressed" "most depressed", "sadness", "depression"]
"angry":["angry","angrier","angriest", "enraged", "pissed off", "piss you off", "anger", "rage"]
"afraid":["afraid", "more afraid", "most afraid", "frightened", "fear", "creepy"]
"disgusted": ["disgusted", "more disgusted", "most disgusted", "grossed out", "most grossed out", "most appalled", "appalled", "disgust"]

Default words not wanted in the title post are:
["song","songs", "film", "films","movie", "movies", "joke", "jokes","lyrics", "book", "books","irrational,unreasonably"]

Additional hand-cleaning of dataset may be needed as some questions can be tricky to catch, such as "Does money buy happiness?"

To test the classification:
