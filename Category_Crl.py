import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from multiprocessing import Pool

def GetCRL():
    main_url ='https://www.10000recipe.com/recipe/list.html'
    req = urllib.request.Request(main_url)
    sourcecode = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    pattern = re.compile('[0-9]+')

    #caturl = soup.find("div", id_="id_search_category").find_all("div", class_="cate_list")  # 해당 상위 속성 범위 좁히기
    caturl = soup.find("div", id="id_search_category").find_all("div", class_="cate_list")
    #print(caturl)
    result = []
    for idx,allca in enumerate(caturl):
        catall = allca.find_all('a')
        # print(idx)

        cat_dict = {}
        for a in catall[1:]:
            #print(a['href'])
            re_str = a['href'].split(',')[1]

            cat_id = pattern.search(re_str).group()
            cat_text = a.text
            cat_dict[cat_id] = cat_text

        result.append(cat_dict)
        # print(cat_dict)
        # print(catall[1])
        # print(catall[1].text)
        #print(x for x in catall[1:] if)

        #[x for x in iterable if 조건]

    return result

# GetCRL()
cat4,cat2,cat3,cat1 = GetCRL()
print(cat4,cat2,cat3,cat1,sep='\n')
# # recipe main page에서 category 별 고유값 추출
# find element cate_list ...
#
# # recipe id 와 id 에 category 정보 추출
# cat1,cat2,cat3,cat4 = {},{},{},{}
#
# base_url = 'url/cat1={}&cat2={}&cat3={}'
# for c1 in cat1:
#     for c2 in cat2:
#         for c3 in cat3:
#             request_url = base_url.format(c1,c2,c3)
#             pagesource = request_url
#             beautifulsoup(pagesource)
#
#             # urllist
#
#
#
# for c4 in cat4
# recipe id 와 id 에 category 정보 추출


# recipe id 별 element 추출