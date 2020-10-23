import sklearn.feature_extraction.text as feature_extract_text

corpus = ["The first time you see The Second Renaissance it may look boring.",
        "Look at it at least twice and definitely watch part 2.",
        "It will change your view of the matrix.",
        "Are the human people the ones who started the war?",
        "Is AI a bad thing ?"]
# initialize count vectorizer object
# use your own tokenize function
vect = feature_extract_text.CountVectorizer()
# get counts of each token (word) in text data
X = vect.fit_transform(corpus)
# convert sparse matrix to numpy array to view
X.toarray()
# view token vocabulary and counts
print(vect.vocabulary_)

