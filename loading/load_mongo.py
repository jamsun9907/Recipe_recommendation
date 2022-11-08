# MongoDB list를 불러오는 함수

from pymongo import MongoClient
import config

def get_con_mongo():
    """
    mongoDB collection을 반환한다.
    """

    # 커넥션 접속 작업
    HOST = config.HOST
    USER = config.USER
    PASSWORD = config.PASSWORD
    DATABASE_NAME = 'recipe_DB'
    COLLECTION_NAME = 'recipe_info_v3'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(MONGO_URI) 
    db = client[DATABASE_NAME] # Connection
    collection = db[COLLECTION_NAME] # Creating table

    return collection

def load_Mongo_recipe():
    """
    MongoDB에 있는 모든 레시피를 불러와 리스트 형태로 반환한다.
    """
    # 커넥션 접속 작업
    collection = get_con_mongo()

    ## MongoDB 에서 데이터 불러오기
    data_list = [i for i in collection.find()]

    return data_list
