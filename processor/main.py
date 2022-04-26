from flask import Flask, render_template, redirect, url_for, request
  
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
    return 'search results ' + search

  

if __name__ == '__main__':
    app.run()