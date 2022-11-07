from flask import Flask, request, render_template
import pandas as pd
import pickle
from model import get_recipe, recommendation_model

app = Flask(__name__) 
model = None 

# Open file (__main__ 이 부분 때문에 절대경로 기입해야 한다.)
# 추가로 class 를 피클링한 경우 그 구조까지는 피클링되지 않기 때문에, 그 클레스를
# 임포트 해야한다.
with open(r"C:\Users\Sunyoung_Jang\Documents\My_project\2022\Recipe_recommendation\recipe.pkl","rb") as fr:
    recipe = pickle.load(fr)
with open(r"C:\Users\Sunyoung_Jang\Documents\My_project\2022\Recipe_recommendation\model.pkl","rb") as fr:
    model = pickle.load(fr)
## recipe는 sql에서 불러올 수 있도록 수정한다

@app.route('/', methods=['GET', 'POST']) 
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        try:
            ###### model training with user input #####
            # input
            try:
                my_ingredients = str(request.form['ingre']) # ''안에 ,로 구분된 입력값을 받는다. (str)
                cooking_time = float(request.form['time']) ## test

            except:
                my_ingredients = '물, 식용유, 밥, 소금, 설탕'
                cooking_time = 180
            
            # training
            model.fit(recipe, my_ingredients)
            pred = model.find_sim_recipe(cooking_time)
            # output = pred[['Recipe_name','Url']].set_index('Recipe_name').to_html()
            output = pred[['Recipe_name','Url']].values.tolist()
            
            # Test
            # for i in output:
            #     print(i)
            return render_template("index.html", recipes=output)

        except :
            return render_template("404.html")

@app.route('/dashboard', methods =['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True)