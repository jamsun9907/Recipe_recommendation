# 정제된 레시피 목록을 localDB에 저장한다.

import config
import pymysql

def get_connection():

    HOST = config.HOST_sql
    USER = config.USER_sql
    PASSWORD = config.PASSWORD_sql
    DB_name='recipe'

    conn = pymysql.connect(host = HOST, user = USER, password = PASSWORD, db = DB_name, charset='utf8') 
    return conn

def init_table(conn):
    """
    recipe Table을 초기화
    """
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS recipe;")
    cur.execute("""CREATE TABLE recipe (
        id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Recipe_name VARCHAR(200),
        Hit_num INTEGER,
        Serves INTEGER,
        Cooking_time INTEGER,
        Difficulty VARCHAR(200),
        Url VARCHAR(200),
        Ingredients VARCHAR(10000));""")
    
    conn.commit()
    pass


def df_to_sql(conn, df_processed):
    """
    레시피 데이터 프레임을 Mysql에 저장
    """
    cur = conn.cursor()
    query = "INSERT INTO recipe(Recipe_name, Hit_num, Serves, Cooking_time, Difficulty, Url, Ingredients) VALUES (%s,%s,%s,%s,%s,%s,%s);"

    for row in range(len(df_processed)):
        data = df_processed.iloc[row, :].tolist()
        cur.execute(query, data)

    conn.commit()
    pass