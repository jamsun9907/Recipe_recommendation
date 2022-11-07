# 레시피 파일을 MongoDB에 저장
from pymongo import MongoClient

def save_on_mongoDB(recipe_info):
    """
    힘들게 구한 레시피 info를 mongoDB에 일단 저장
    """
    HOST = NONE
    USER = NONE
    PASSWORD = NONE
    DATABASE_NAME = 'recipe_DB'
    COLLECTION_NAME = 'recipe_info_v3'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    # 커넥션 접속 작업
    client = MongoClient(MONGO_URI) 
    db = client[DATABASE_NAME] # Connection
    collection = db[COLLECTION_NAME] # Creating table

    collection.insert_one(document = recipe_info)

    return None
