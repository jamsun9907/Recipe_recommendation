from itertools import chain
from pymongo import MongoClient
import pandas as pd
import pickle
import os
import config
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class get_recipe:
    '레시피 데이터를 불러온다.'

    def load_Mongo_recipe(self):
        """
        MongoDB에 있는 모든 레시피를 불러와 리스트 형태로 반환한다.
        """
        # 커넥션 접속 작업
        HOST = config.HOST
        USER = config.USER
        PASSWORD = config.PASSWORD
        # HOST = os.getenv('HOST')
        # USER = os.getenv('USER')
        # PASSWORD = os.getenv('PASSWORD')
        DATABASE_NAME = 'recipe_DB'
        COLLECTION_NAME = 'recipe_info_v3'
        MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

        client = MongoClient(MONGO_URI) 
        db = client[DATABASE_NAME] # Connection
        collection = db[COLLECTION_NAME] # Creating table

        ## MongoDB 에서 데이터 불러오기
        data_list = [i for i in collection.find()]

        return data_list

    def list_to_dataframe(self, data_list):
        """
        list를 넣어주면 더블리스트 풀고 df에 추가한다.
        전처리는 덤
        """
        # 데이터 프래임 생성
        df = pd.DataFrame(
        {'Recipe_name':[],
        'Hit_num':[],
        'Serves':[],
        'Cooking_time':[],
        'Difficulty':[],
        'Url':[],
        'Ingredients':[]})

        for row in range(len(data_list)):
            try:
                # 재료의 더블 리스트롤 풀어준다
                dict_val = data_list[row]['ingredients'].values()
                ingredients = ','.join(s for s in list(chain(*dict_val))) # 리스트를 텍스트로 변환

                # 데이터 프레임에 추가 (id, name, url, ingredient 순서)
                df.loc[row] = [
                    data_list[row]['recipe_name'], 
                    data_list[row]['hit_num'],
                    data_list[row]['serves'],
                    data_list[row]['cooking_time'], 
                    data_list[row]['difficulty'],
                    data_list[row]['url'], 
                    ingredients]
            except: 
                pass 
                # print(data_list[row], type(data_list[row]['ingredients'])) # 재료를 입력 안한 경우. 무시하면 될 듯
        
        # 결측값 제거 중복 제거 및 재정렬
        df.drop_duplicates(subset='Url', inplace = True)
        df.dropna(inplace=True)
        # print(df.isna().sum().sum())
        df.reset_index(inplace = True, drop = True)

        # 컬럼 형식 맞추기
        df['Hit_num'] = df['Hit_num'].str.replace(',','').astype(int)
        df['Serves'] = df['Serves'].str.extract(r'(\d+)').astype(int)
        df['Cooking_time'] = df['Cooking_time'].str.replace('2시간','120').str.extract(r'(\d+)').astype(int)

        return df


    def just_get(self):
        """
        MongoDB에 저장된 recipe를 데이터 프래임 형태로 불러온다.
        """

        data = self.load_Mongo_recipe()
        recipe_df = self.list_to_dataframe(data)
        return recipe_df

    # def info(self, recipe_df):
    #     """
    #     저장된 레시피 정보를 불러오는 함수
    #     """
    #     print(recipe_df.info())
    #     print(f'\n\n------------\n저장된 레시피 : {recipe_df.shape[0]}개')
    #     return None


class recommendation_model:
    """
    Input
    df : DB에 저장된 레시피(df형태)
    my_ingredients_list : 입력 안하면 '물, 쌀, 밥, 소금, 식용유, 김치'
    cooking_time : 입력 안하면 최대치

    attribute 
    recipes : fit이 완료된 레시피를 반환한다. 
    my_ingredients_list : 입력한 레시피 리스트를 반환한다.
    """

    def __init__(self, df):
        self.recipes = None
        self.df = df
        self.my_ingredients_list = None
        self.cooking_time = None
    # 얘가 사실상 모델에 가장 가깝지 않을까...

    def fit(self, my_ingredients_list='물, 쌀, 밥, 소금, 식용유, 김치', cooking_time = 1000):
        """
        my_ingredients_list, cooking_time을 입력하면 
        데이터프레임의 Cosine similarity를 계산하여 학습한다.
        """
        # 레시피 복사
        df_recipe = self.df.copy()
        self.my_ingredients_list = my_ingredients_list
        self.cooking_time = cooking_time

        # Embedding
        my_ingredients = [self.my_ingredients_list]
        recipe_ingre_list = list(df_recipe['Ingredients'])

        doc_list = my_ingredients + recipe_ingre_list
        
        vect = CountVectorizer(lowercase=False)
        ingredients_mat = vect.fit_transform(doc_list)

        # Cosine similarity
        similarity = cosine_similarity(ingredients_mat[0], ingredients_mat[1:]) # 내 재료, 레시피 재료
        df_recipe['similarity'] = similarity.reshape(-1)

        self.recipes = df_recipe
        
        return None

    def find_sim_recipe(self):
        """
        내가 가진 재료와 비슷한 레시피를 반환한다.
        레시피에 중복이 있을 경우 더 조회수가 높은 레시피를 반환한다.
        """
        
        # Contents based recommendation    
        result = self.recipes.sort_values(by = 'similarity', ascending = False)

        ## 사용자 희망 조리시간에 맞게 결과 반환
        recommandation = result[result['Cooking_time'] <= self.cooking_time].head(20)

        # 중복 레시피는 조회수 높은 것으로 필터링
        recommandation = recommandation.sort_values(by = 'Hit_num', ascending = False).drop_duplicates(subset = 'Recipe_name', keep = 'first').head(10)

        return recommandation

# pickling
recipe_class = get_recipe()
recipes = recipe_class.just_get()
# with open('recipe.pkl','wb') as f:
#     pickle.dump(recipe, f)

model = recommendation_model(recipes)
with open('model.pkl','wb') as f:
    pickle.dump(model, f)

# with open(r"C:\Users\Sunyoung_Jang\Documents\My_project\2022\Recipe_recommendation\recipe.pkl","rb") as fr:
#     recipe = pickle.load(fr)

# print(type(recipe),recipe)