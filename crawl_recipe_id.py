import time
import pandas as pd
import urllib.request
from itertools import count
from bs4 import BeautifulSoup
from multiprocessing import Pool

# 초기 url 여기에 cat id를 합친다
base_url = 'https://www.10000recipe.com/recipe/list.html?cat1={}&cat2={}&cat3={}'
def Crawl_recipe_id(c1):
    recipe_list = []
    for c2 in cat2:
        for c3 in cat3:
            for page_idx in count(1):
                pageurl = base_url.format(c1,c2,c3) + '&page=' + str(page_idx)
                sourcecode = urllib.request.urlopen(pageurl).read()
                soup = BeautifulSoup(sourcecode, "html.parser")
                # print(pageurl)
                allrcp = soup.find("div", class_="row").find_all("div", class_="col-xs-3")  # 해당 상위 속성 범위 좁히기
                '''
                #print(allrsp.find("a")["href"])
                #print(type(allrcp))
                #print('-'*60)
                #print(allrsp)
                '''
                if allrcp :
                    baseurl = 'https://www.10000recipe.com/'
                    for idx in allrcp:
                        print('-'*60)
                        if idx.find('a') == None: # A태그에 해당안되어 None 값으로 리턴되는 결과 제외
                            pass
                        else:
                            recipe_id = idx.find('a')['href'].split('/')[2]
                            recipe_list.append({'id':recipe_id,'cat1':c1,'cat2':c2,'cat3':c3})
    # end for

    return recipe_list # 1페이지당 레시피의 결과물





if __name__=='__main__':
    cat1 = {}
    cat2 = {}
    cat3 = {}
    cat4 = {}
    print('크롤링 시작')
    start_time = time.time()
    pool = Pool(processes=16) # 4개의 프로세스를 사용합니다

    result_list = pool.map(Crawl_recipe_id,cat1.keys()) # get_contetn 함수를 넣어줍시다.
    end = []
    [end.extend(i) for i in result_list]
    df = pd.DataFrame(end)
    df.to_csv('Crawl_recipe_id.csv', encoding='UTF-8', header=True)
    print("--- %s seconds ---" % (time.time() - start_time))

