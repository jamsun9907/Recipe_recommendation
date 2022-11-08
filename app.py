from flask import Flask, request, render_template
import pandas as pd
import pickle
from model import recommendation_model

app = Flask(__name__) 

# Flask
with open("model.pkl","rb") as fr:
    model = pickle.load(fr)


# Open file (__main__ 이 부분 때문에 절대경로 기입해야 한다.)
# 추가로 class 를 피클링한 경우 그 구조까지는 피클링되지 않기 때문에, 그 클레스를
# 임포트 해야한다.

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
                cooking_time = int(request.form['time'])

            except:
                my_ingredients = '물, 식용유, 밥, 소금, 설탕'
                cooking_time = 180
            
            # Training
            model.fit(my_ingredients, cooking_time)

            # Recommendation
            recommendation = model.find_sim_recipe()

            # Export
            output = recommendation[['Recipe_name','Url']].values.tolist()
            return render_template("index.html", recipes=output, my_ingredients=my_ingredients, cooking_time=cooking_time)

        except :
            return render_template("404.html")

@app.route('/dashboard', methods =['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)