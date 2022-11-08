## MongoDB 데이터 불러와 전처리 후 mysql에 적재, 데이터 프레임 반환

from store_sql import get_connection, init_table, df_to_sql
from preprocessing import simple_processing
from load_mongo import load_Mongo_recipe

# MongoDB 데이터 불러오기 
data_list = load_Mongo_recipe()

# Data -> Dataframe
df = simple_processing(data_list)

# Sql 적재
conn = get_connection()
init_table(conn)
df_to_sql(conn, df)