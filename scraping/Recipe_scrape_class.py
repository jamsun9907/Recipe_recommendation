# 파일명 : Recipe_scrape_class.py

import time
from requests import get
from bs4 import BeautifulSoup
import numpy as np

class recipe_10000():
    """ 이 클레스는 레시피 코드를 입력하면 세부사항을 반환한다. 
    레시피는 아래의 properties를 갖는다:
    Attributes:
        url: 만개의 레시피 url
    Methods:
        Ingredients: 레시피 재료들(재료, 주재료, 부재료 등)
        Cooking time: 조리시간(분)
        Difficulty: 레시피 난이도
        Serves: 몇인분
    """
    def __init__(self, recipe_code):
        self.url = f'https://www.10000recipe.com/recipe/{recipe_code}'
        self.soup = BeautifulSoup(get(self.url).content, 'html.parser')
    
    def recipe_name(self):
        """ 레시피 명"""
        # Some of the urls are not recipe urls so to avoid errors we use try/except 
        try:
            return self.soup.find(id = 'relationGoods').find("div", 'best_tit').b.text
        except: 
            return np.nan

    def hit_num(self):
        """ 해당 레시피 조회수 """
        try:
            return self.soup.find("span", 'hit font_num').contents[0]
        except:
            return np.nan 

    def serves(self):
        """ 몇인분 """
        try:
            return self.soup.find("span", 'view2_summary_info1').contents[0]
        except:
            return np.nan 

    def cooking_time(self):
        """ 조리시간(분) """
        try:
            return self.soup.find("span", 'view2_summary_info2').contents[0]
        except:
            return np.nan


    def difficulty(self):
        """ 난이도 """
        try:
            return self.soup.find("span", 'view2_summary_info3').contents[0]
        except:
            return np.nan

    def ingredients(self):
        """ 레시피 재료들(재료, 주재료, 부재료 등)을 딕셔너리 형태로 반환 """
        try:
            ingredients_dict = {}
            ingredients = self.soup.find(id = 'divConfirmedMaterialArea').find_all('ul')

            for tb_num in range(len(ingredients)):
                # 재료 종류(재료, 주재료, 양념 등)
                tb_name = ingredients[tb_num].b.contents[0].replace('[','').replace(']','')
                
                # 재료 종류에 맞는 재료
                ingre_list = [ingregient.contents[0].strip() for ingregient in ingredients[tb_num].find_all('li')] 

                # 딕셔너리 형태로 저장
                ingredients_dict[tb_name] = ingre_list # 딕셔너리 형태로 저장
            return ingredients_dict

        except:
            return np.nan

def recipe_finder(recipe_code, flag = False):
    """
    레시피 코드를 입력하면 레시피명, 재료, 링크를 반환한다.
    """
    # 트레픽 조절
    if flag is True:
        time.sleep(1) 

    # 레시피 페이지 정보
    recipe_page = recipe_10000(recipe_code)
    
    # 딕셔너리 형태로 저장
    recipe_info = {}

    recipe_info['recipe_name'] = recipe_page.recipe_name()
    recipe_info['hit_num'] = recipe_page.hit_num()
    recipe_info['serves'] = recipe_page.serves()
    recipe_info['difficulty'] = recipe_page.difficulty()
    recipe_info['url'] = recipe_page.url
    recipe_info['ingredients'] = recipe_page.ingredients()
    
    return recipe_info