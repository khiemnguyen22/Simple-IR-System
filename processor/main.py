from flask import Flask, render_template, redirect, url_for, request
from query_processor import *
import sys
sys.path.append('../')
from indexer.inverted_index import *

app = Flask(__name__)
  
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/search",methods =['POST','GET'])
def search():
    if request.method == 'POST':
        input = request.form['search']
        return redirect(url_for('result',search = input))
    else:
      input = request.args.get('search')
      return redirect(url_for('result',search = input))

@app.route("/result/<search>")
def result(search):
    index = load_index('../indexer/cs_courses.pickle')
    corpus, urls = load_corpus_file('../indexer/corpus.txt'), load_urls('../indexer/urls.txt')
    results = ''
    K = 10

    # search = spelling_correction(search)[:-1]
    query = modify_query(search, get_vocab(index))[:-1]
    vector = query_to_vector(query, index, len(corpus))
    matches = cos_similarity(vector, index, corpus)
    print(query)
    print(matches[:K])
    for i in range(K):
        results += urls[matches[i][0]] + '\n'
    
    return render_template('results.html', **locals())

  

if __name__ == '__main__':
    app.run()