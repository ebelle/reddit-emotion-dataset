# reddit-emotion-dataset
Creates an emotion dataset using responses to AskReddit questions such as "what makes you happy?"

To use the scraper, you need reddit credentials, which can be obtained here: https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform and then they should be put into a yaml file. It should look like this: <br />
<br />
--- <br />
id: 'youridhere' <br />
secret: 'yoursecrethere'<br />
agent: 'youragenthere' <br />
...<br />
<br />
The scraper can be run as:<br />

python reddit_scraper.py --save-path data/ \
--reddit-credentials credentials.yaml

The default emotions and search terms are shown below. They can be updated with the --emotion-dict flag:
<br />
{"happy":["happy","happier", "happiest", "ecstatic", "pleasure","joy", "joyful", "joyous","happiness"],<br />
"surprised":["surprised", "more surprised", "most surprised", "shocked", "most shocked","surprise", "biggest surpise", "shock"],<br />
"sad": ["sad", "sadder", "saddest", "depressed", "more depressed" "most depressed", "sadness", "depression"],<br />
"angry":["angry","angrier","angriest", "enraged", "pissed off", "piss you off", "anger", "rage"],<br />
"afraid":["afraid", "more afraid", "most afraid", "frightened", "fear", "creepy"],<br />
"disgusted": ["disgusted", "more disgusted", "most disgusted", "grossed out", "most grossed out", "most appalled", "appalled", "disgust"]}

The following title terms are excluded from the titles. They can be updated with the --excluded-words flag:<br />
["song","songs", "film", "films","movie", "movies", "joke", "jokes","lyrics", "book", "books","irrational","unreasonably"]

To test out classification:

python classify.py --filename data/comments.json \
--tfidf --empath --char-features --classifier sgd