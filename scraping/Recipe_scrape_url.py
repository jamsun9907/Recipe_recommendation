# 파일명 : Recipe_scrape_url.py

import time
from requests import get
from bs4 import BeautifulSoup

def get_total_recipe_list(page_num = 1, flag = False):
    """
    page number를 입력하면 만개의레시피에서 해당 페이지 레시피들(40개)의 레시피 코드를 Scrape 하여 list로 반환한다.
    flag : True로 설정할 경우 Time sleep == 1 로 활성화된다.
    """
    # 트레픽 조절
    if flag is True:
        time.sleep(1) 

    # 만개의레시피 웹사이트 (400페이지까지 스크레핑)
    url = f'https://www.10000recipe.com/recipe/list.html?order=reco&page={page_num}'
    html = get(url) # Response [200]
    soup = BeautifulSoup(html.content, 'html.parser')

    # 페이지에서 각 레시피의 url을 가져옴
    recipe_list = soup.find_all('a','common_sp_link', href=True)

    # 한 페이지 당 레시피의 개수(40개)
    recipe_num = len(recipe_list) 

    # 페이지에서 각 레시피 url 끝자리의 레시피 코드를 가져온다.
    recipe_code_list = []

    for i in range(recipe_num):
        code = recipe_list[i]['href'].split('recipe/')[1]
        try:
            # 정수로 변환 후 저장
            code = int(code)
            recipe_code_list.append(code)
        except:
            # Debug
            print(f"Error : {i}번째 파싱 실패\n문제 url : {recipe_list[i]['href']}")
            pass
    return recipe_code_list