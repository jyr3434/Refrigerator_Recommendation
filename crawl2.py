import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

recfile = '.././Yori/recipe.csv'
data = pd.read_csv(recfile, encoding='euc-kr', index_col=1, sep=',')
#print(data)

data = pd.DataFrame(data)
#print(data[2:3].spl)
print(data.shape)
print(data[1:1][0])
#newcol = ['ment']
# newdata = data.reindex(columns= newcol)
#
# print(newdata)
# text = open(recfile, 'rt', encoding='euc-kr')
# text = text.read()
# print(text)


