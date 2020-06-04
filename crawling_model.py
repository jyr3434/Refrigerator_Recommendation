import re,time,urllib.request
import pandas as pd
from itertools import count
from bs4 import BeautifulSoup
from bs4 import element
from multiprocessing import Pool

class Crawl:
    # 초기 url 여기에 cat id를 합친다
    main_url = 'https://www.10000recipe.com/recipe/list.html'
    base_url = 'https://www.10000recipe.com/recipe/list.html?cat1={}&cat2={}&cat3={}'
    cat4_url = 'https://www.10000recipe.com/recipe/list.html?cat4={}'
    def __init__(self):
        self.cat1,self.cat2,self.cat3,self.cat4 = {},{},{},{}

    def GetCRL(self):

        req = urllib.request.Request(self.main_url)
        sourcecode = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(sourcecode, "html.parser")

        pattern = re.compile('[0-9]+')

        caturl = soup.find("div", id="id_search_category").find_all("div", class_="cate_list")

        result = []
        for allca in caturl:
            catall = allca.find_all('a')


            cat_dict = {}
            for a in catall[1:]:
                #print(a['href'])
                re_str = a['href'].split(',')[1]
                cat_id = pattern.search(re_str).group()
                cat_text = a.text
                cat_dict[cat_id] = cat_text

            result.append(cat_dict)


        self.cat4, self.cat2, self.cat3, self.cat1 =  result




    def Crawl_recipe_id(self,c1):

        recipe_list = []
        for c2 in self.cat2.keys():
            for c3 in self.cat3.keys():
                for page_idx in count(1):
                    pageurl = self.base_url.format(c1,c2,c3) + '&page=' + str(page_idx)
                    print(pageurl)
                    sourcecode = urllib.request.urlopen(pageurl).read()
                    soup = BeautifulSoup(sourcecode, "html.parser")
                    # print(pageurl)
                    col_xs_list = soup.select("div.col-xs-3")  # 해당 상위 속성 범위 좁히기
                    '''
                    #print(allrsp.find("a")["href"])
                    #print(type(allrcp))
                    #print('-'*60)
                    #print(allrsp)
                    '''

                    if len(col_xs_list)>1 : # 검색 결과가 있습니다.
                        for col_xs in col_xs_list:
                            print('-'*60)

                            a = col_xs.select_one('a.thumbnail')
                            if a:
                                recipe_id = a['href'].split('/')[2]
                                print(recipe_id)
                                recipe_list.append({'id':recipe_id,\
                                                    'cat1':self.cat1[c1],\
                                                    'cat2':self.cat2[c2],\
                                                    'cat3':self.cat3[c3]})
                    else: # 검색결과가 없습니다
                        break
        # end for
        return recipe_list # 1페이지당 레시피의 결과물

    def Crawl_recipe_id_by_cat4(self,c4):

        recipe_list = []

        for page_idx in count(1):
            pageurl = self.cat4_url.format(c4) + '&page=' + str(page_idx)
            print(pageurl)
            sourcecode = urllib.request.urlopen(pageurl).read()
            soup = BeautifulSoup(sourcecode, "html.parser")
            # print(pageurl)
            col_xs_list = soup.select("div.col-xs-3")  # 해당 상위 속성 범위 좁히기
            '''
            #print(allrsp.find("a")["href"])
            #print(type(allrcp))
            #print('-'*60)
            #print(allrsp)
            '''

            if len(col_xs_list)>1 : # 검색 결과가 있습니다.
                for col_xs in col_xs_list:
                    print('-'*60)

                    a = col_xs.select_one('a.thumbnail')
                    if a:
                        recipe_id = a['href'].split('/')[2]
                        print(recipe_id)
                        recipe_list.append({'id':recipe_id,\
                                            'cat4':self.cat4[c4]
                                            })
            else: # 검색결과가 없습니다
                break
        # end for
        return recipe_list # 1페이지당 레시피의 결과물



if __name__=='__main__':
    crawl = Crawl()
    crawl.GetCRL()
    print(crawl.cat4, crawl.cat2, crawl.cat3, crawl.cat1, sep='\n')
    print('크롤링 시작')
    start_time = time.time()
    # pool = Pool(processes=16) # 4개의 프로세스를 사용합니다

    # result_list = pool.map(crawl.Crawl_recipe_id,iter(crawl.cat1.keys())) # get_contetn 함수를 넣어줍시다.
    # end = []
    # [end.extend(i) for i in result_list]
    # df = pd.DataFrame(end)
    # df.to_csv('crawl_data/crawl_recipe_id.csv', encoding='UTF-8', header=True)

    # result_list = pool.map(crawl.Crawl_recipe_id_by_cat4,iter(crawl.cat4.keys()))
    # end = []
    # [end.extend(i) for i in result_list]
    # df = pd.DataFrame(end)
    # df.to_csv('crawl_data/cat4.csv', encoding='UTF-8', header=True)

    df1 = pd.read_csv('crawl_data/crawl_recipe_id.csv',index_col=0)
    df2 = pd.read_csv('crawl_data/cat4.csv',index_col=0)
    df3 = pd.merge(df1,df2,on='id')
    df3.to_csv('crawl_data/id_4category.csv',encoding='UTF-8',header=True)
    print("--- %s seconds ---" % (time.time() - start_time))