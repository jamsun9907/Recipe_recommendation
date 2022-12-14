from itertools import chain
import pandas as pd
import numpy as np


def list_to_dataframe(data_list):
    """
    list를 넣어주면 더블리스트 풀고 df에 추가한다.
    Mongo DB에 있던 중복치 처리는 덤
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
        except: pass #print(data_list[row], type(data_list[row]['ingredients'])) # 재료를 입력 안한 경우. 무시하면 될 듯

    return df


def preprocessing(df):
    """
    깔끔하게 전처리를 완료하는 함수이다.
    """
    df_clean = df.copy()

    # na 제거, 중복 제거 및 재정렬
    df_clean = df.copy()
    df_clean.dropna(inplace=True)
    df_clean.drop_duplicates(subset='Url', inplace = True)
    df_clean.reset_index(inplace = True, drop = True)

    # 컬럼 형식 맞추기
    df_clean['Hit_num'] = df_clean['Hit_num'].str.replace(',','').astype(int)
    df_clean['Serves'] = df_clean['Serves'].str.extract(r'(\d+)').astype(int)
    df_clean['Cooking_time'] = df_clean['Cooking_time'].str.replace('2시간','120').str.extract(r'(\d+)').astype(int)

    return df_clean

def text_processing(df_clean):
    """
    자연어 처리 배우고 나서 재료 텍스트 전처리
    """
    pass

def simple_processing(data_list):
    """
    MongoDB에서 불러온 리스트를 넣으면 전처리된 Dataframe을 반환한다.
    data_list : load_Mongo_recipe() 로 불러진 데이터
    """    
    df = list_to_dataframe(data_list)
    df_clean = preprocessing(df)
    # 텍스트 전처리 추가하기.

    return df_clean