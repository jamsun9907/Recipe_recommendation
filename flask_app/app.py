from flask import Flask, request, render_template
import pickle

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
        return '<h3>Hi, heroku!</h3>'
        # return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)