import numpy as np
import nltk
from collections import defaultdict
from itertools import groupby
import pickle
nltk.download('words')
from nltk.corpus import words
correct_words = words.words()

def load_index(pickle_file):
    with open(pickle_file, 'rb') as f:
        dict = pickle.load(f)
    return dict

def load_corpus_file(corpus_file):
    with open(corpus_file, 'r') as f:
        lines = f.readlines()
    return lines
    
def load_urls(url_file):
    with open(url_file, 'r') as f:
        lines = f.readlines()
    return lines

def get_vocab(index):
    return [term for term in index.keys()]

def spelling_correction(query):
    corrected_query = ''
    for word in query.split():
        temp = [(nltk.edit_distance(word, w),w) for w in correct_words if w[0]==word[0]]
        corrected_query += sorted(temp, key = lambda val:val[0])[0][1] + ' '
    return corrected_query


def modify_query(query, vocab):
    query_terms = query.split() 
    modified_query = ''
    for term in query_terms:
        match = vocab[0]
        min_dst = nltk.edit_distance(term, match)
        for i in range(1, len(vocab)):
            dst = nltk.edit_distance(term, vocab[i])
            if  dst < min_dst:
                min_dst = dst
                match = vocab[i]
        modified_query += match + ' '
    
    return modified_query

