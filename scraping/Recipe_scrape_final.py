# 파일명 : Recipe_scrape_final.py

from Recipe_scrape_url import get_total_recipe_list
from Recipe_scrape_class import recipe_10000, recipe_finder
from Recipe_store import on_mongoDB


# 1000page까지 가보자
for i in range(1,2):
    print(f'{i}번째 페이지 스크래핑 중...\n')
    recipe_list = get_total_recipe_list(page_num = i) # 

    for recipe in recipe_list:
        try:
            recipe_info = recipe_finder(recipe)
            on_mongoDB(recipe_info)
        except:
            print(f'\n-----------------------\nError! Sth wrong happened in recipe_code : {recipe}')
            pass
            
    print(f"""
Result:
{i}번째 페이지 스크래핑 완료
MongoDB 예상 적재 데이터 : {40 * i}개
    --------------------------------------
    """)