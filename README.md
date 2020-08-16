# reddit-emotion-dataset
Creates a emotion dataset using responses to AskReddit questions such as "what makes you happy?"

To use the scraper, you need a yaml file with your reddit credentials. It can be run as:

bash
python reddit_scraper.py --save-path ../data/ \
--reddit-credentials credentials.yaml

Title search terms can be changed by creating your own --emotion-dict for the scraper. Defaults are :<br />
"happy":["happy","happier", "happiest", "ecstatic", "pleasure","joy", "joyful", "joyous","happiness"]<br />
"surprised":["surprised", "more surprised", "most surprised", "shocked", "most shocked","surprise", "biggest surpise", "shock"]<br />
"sad": ["sad", "sadder", "saddest", "depressed", "more depressed" "most depressed", "sadness", "depression"]<br />
"angry":["angry","angrier","angriest", "enraged", "pissed off", "piss you off", "anger", "rage"]<br />
"afraid":["afraid", "more afraid", "most afraid", "frightened", "fear", "creepy"]<br />
"disgusted": ["disgusted", "more disgusted", "most disgusted", "grossed out", "most grossed out", "most appalled", "appalled", "disgust"]

 Words not wanted in the title can be changed by creating your own --excluded-words list. Defaults are:<br />
["song","songs", "film", "films","movie", "movies", "joke", "jokes","lyrics", "book", "books","irrational,unreasonably"]

Additional hand-cleaning of dataset may be needed as some questions, such as "Does money buy happiness?", can be tricky to catch.

To test the classification:

bash 
python classify.py --filename data/2018.08.08_comments.json \
--char-features --tfidf --empath --vader --sliding-window --bigrams \
--classifier svc
