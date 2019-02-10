"""
    filename: movies.py

    description:
        Performs sentiment analysis on text to determine positive or negative
        Trained on NLTK movie review data, uses Naive Bayes Classifier
        
    author:
        Dylan P. Jackson
"""

import nltk, random

from nltk.corpus import movie_reviews

from nltk import sentiment

def main():

    documents = [(list(movie_reviews.words(fileid)), category) for category in
                    movie_reviews.categories() for fileid in 
                    movie_reviews.fileids(category)]

    random.shuffle(documents)
   
    # Gets 2000 most common words from corpus 
    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    word_features = list(all_words)[:2000]
   
    # Of 2000 most common words, pull them from each document and associate 
    # critique to it/them
    featuresets = [(document_features(d, word_features), c) 
                    for (d,c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print(nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(10)

    sentiment_analyser = nltk.sentiment.SentimentAnalyzer(classifier)
    test_doc = ['Trump'] 
    result = sentiment_analyser.classify(test_doc)
    print(result)
    

# Feature extractor 
def document_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


main()
