from flask import Flask, request, render_template
import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__) 
model = None 

with open("recipe.pickle","rb") as fr:
    recipe = pickle.load(fr)
with open("model.pickle","rb") as fr:
    model = pickle.load(fr)
## recipe는 sql에서 불러올 수 있도록 수정한다

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True)