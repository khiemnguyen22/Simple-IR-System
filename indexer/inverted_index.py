import argparse
import math
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pickle

def load_corpus(json_file):
    f = open('../crawler/'+json_file)
    data = json.load(f)
    corpus = []
    for obj in data:
        doc = obj['code'] + '\n title: '+obj['title'] +'\n credits: ' + obj['credits'] + '\n description: '+obj['description'] + '\n prerequisites: ' 
        for course in obj['prerequisites:']:
            doc += course +' '
        corpus.append(doc)
    return corpus


def tf_idf_index(corpus):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus).toarray()
    feature_names = vectorizer.get_feature_names()
    tfidf_index = {}
    for i in range(len(feature_names)):
        tfidf_index[feature_names[i]] = []
        for doc in range(len(corpus)):
            if X[doc][i] > 0:
                tfidf_index[feature_names[i]].append((doc, X[doc][i]))
    
    return tfidf_index

def query_to_vector(query, inv_index, N):
    terms = query.split(" ")
    vector = {}
    for term in terms:
        if term not in inv_index:
            vector[term] = 0
        else:
            df = len(inv_index[term])
            idf = math.log(N / df)
            vector[term] = idf
    return vector

def cos_similarity(query_vector, tfidf_index, corpus):
    scores = {}
    for i in range(len(corpus)):
        scores[i] = 0
    for term in query_vector:
        for (doc, score) in tfidf_index[term]:
            scores[doc] += score * query_vector[term]
    for doc in scores.keys():
        scores[doc] = scores[doc] / len(corpus[doc])

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def to_pickle(index, output_file):
    with open(output_file, "wb") as file:
        pickle.dump(index, file)
    file.close()
    print('saved to ', output_file)

def main(args):
    corpus = load_corpus(args.json_file)
    N = len(corpus)
    index = tf_idf_index(corpus)
    print(index)
    to_pickle(index, args.output_file)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inverted index construction')

    # Example command
    parser.add_argument('--json_file', type=str, default='cs_courses.json')
    parser.add_argument('--output_file', type=str, default='cs_courses.pickle')
    main(parser.parse_args())