# 파일명 : Recipe_scrape_final.py

from Recipe_scrape_url import get_total_recipe_list
from Recipe_scrape_class import recipe_10000, recipe_finder
from Recipe_store import save_on_mongoDB

import time
start = time.time()  # 시작 시간 저장


# 1000page까지 가보자
# 현재까지 40페이지 완료 200페이지까지 진행중
for i in range(1, 201):
    print(f'Scraping {i}th page...\n')
    
    recipe_list = get_total_recipe_list(page_num = i) # 
    print(f'Status : recipe list are collected from the page')

    cnt = 0
    for recipe in recipe_list:
        try:
            recipe_info = recipe_finder(recipe, flag = True)
            save_on_mongoDB(recipe_info)
            print(f'Status : {recipe_info["recipe_name"]} Done')  # status 확인/
            cnt += 1
        except:
            print(f'-----------------------\nError! Sth wrong happened in recipe_code : {recipe}') # 보통 에러 발생하는건 response 문제이다
            pass 
            
    print(f"""
    Result:
    Scraping done : {i}th page
    # of stored data on MongoDB : {cnt}
    --------------------------------------
        """)

print(f"""
All processes are done
time : {time.time() - start}
""")