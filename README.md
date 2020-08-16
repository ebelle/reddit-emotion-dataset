# reddit-emotion-dataset
Creates a emotion dataset using responses to AskReddit questions such as "what makes you happy?"

To use the scraper, you need reddit credentials, which can be obtained here: https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform and then they should be put into a yaml file.
The scraper can be run as:

bash
python reddit_scraper.py --save-path data/ \
--reddit-credentials credentials.yaml

If you'd like to hand clean the titles being scraped first, use the --titles-only flag. This will return a csv with the titles of all the posts to be scraped. After cleaning, in order to get the comments, run the scraper again with:

bash
python reddit_scraper.py --save-path data/ \
--get-comments data/titles.csv \
--reddit-credentials credentials.yaml

Title search terms can be changed by creating your own --emotion-dict for the scraper. Default dictionary is :<br />
{"happy":["happy","happier", "happiest", "ecstatic", "pleasure","joy", "joyful", "joyous","happiness"],<br />
"surprised":["surprised", "more surprised", "most surprised", "shocked", "most shocked","surprise", "biggest surpise", "shock"],<br />
"sad": ["sad", "sadder", "saddest", "depressed", "more depressed" "most depressed", "sadness", "depression"],<br />
"angry":["angry","angrier","angriest", "enraged", "pissed off", "piss you off", "anger", "rage"],<br />
"afraid":["afraid", "more afraid", "most afraid", "frightened", "fear", "creepy"],<br />
"disgusted": ["disgusted", "more disgusted", "most disgusted", "grossed out", "most grossed out", "most appalled", "appalled", "disgust"]}

 Words not wanted in the title can be changed by creating your own --excluded-words list. Defaults are:<br />
["song","songs", "film", "films","movie", "movies", "joke", "jokes","lyrics", "book", "books","irrational","unreasonably"]


To test the classification:

bash 
python classify.py --filename data/comments.json \
--char-features --tfidf --vader \
--classifier svc
