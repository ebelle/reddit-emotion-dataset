# reddit-emotion-dataset
Creates a emotion dataset using responses to AskReddit questions such as "what makes you happy?"

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

The default emotions and search terms are shown below:
<br />
{"happy":["happy","happier", "happiest", "ecstatic", "pleasure","joy", "joyful", "joyous","happiness"],<br />
"surprised":["surprised", "more surprised", "most surprised", "shocked", "most shocked","surprise", "biggest surpise", "shock"],<br />
"sad": ["sad", "sadder", "saddest", "depressed", "more depressed" "most depressed", "sadness", "depression"],<br />
"angry":["angry","angrier","angriest", "enraged", "pissed off", "piss you off", "anger", "rage"],<br />
"afraid":["afraid", "more afraid", "most afraid", "frightened", "fear", "creepy"],<br />
"disgusted": ["disgusted", "more disgusted", "most disgusted", "grossed out", "most grossed out", "most appalled", "appalled", "disgust"]}

You can use your own search terms with the --emotion-dict flag. Each key in the dictionary is the primary emotion and other words are synonyms to search for. If you'd like to make changes, I suggest copying the default dictionary below, editing it, and pasting it after the --emotion-dict flag.<br />

Similarly you can exclude title terms using the --excluded-words flag. Defaults are:<br />
["song","songs", "film", "films","movie", "movies", "joke", "jokes","lyrics", "book", "books","irrational","unreasonably"]

To test out classification:

python classify.py --filename data/comments.json \
--tfidf --empath -char-features
