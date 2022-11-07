from flask import Flask, request, render_template
import pickle
import os

app = Flask(__name__) 
model = None 

# with open(r"C:\Users\Sunyoung_Jang\Documents\GitHub\Projects\Recipe_recommendation\flask_app\recipe.pickle","rb") as fr:
#     recipe = pickle.load(fr)
# with open(r"C:\Users\Sunyoung_Jang\Documents\GitHub\Projects\Recipe_recommendation\flask_app\model.pickle","rb") as fr:
#     model = pickle.load(fr)
## recipe는 sql에서 불러올 수 있도록 수정한다

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'GET':
        return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True)