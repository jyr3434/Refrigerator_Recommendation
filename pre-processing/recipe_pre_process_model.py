import pandas as pd
import cx_Oracle

class RecipePreProcess:
    def __init__(self):
        pass

    def concat_data(self,x,y):
        return pd.concat([x,y],axis=0,ignore_index=True)
    def merge_data(self,x,y):
        return pd.merge(x,y,how='inner',left_on='id',right_on='recipe_id')

    # 파일명과 데이터 프레임을 넣어 준다.
    def save_data(self,filename,df):
        if isinstance(df,pd.DataFrame):
            # 파일명, 데이터의 범위를 표시해준다.
            df.to_csv('crawl_data/{}_0_{}.csv'.format(filename,len(df)),encoding='utf-8')
        else:
            print('argument type not dataframe')

    # 해당 데이터프레임을 oracle table에 insert한다.
    def df_to_oracle(self,df):
        if isinstance(df,pd.DataFrame):
            pass
        else:
            print('argument type not dataframe')


if __name__ == '__main__':
    recipepp = RecipePreProcess()
    # df1 = pd.read_csv('crawl_data/recipe_info_0_60000.csv',index_col=0)
    # df2 = pd.read_csv('crawl_data/recipe_info_60000_135345.csv',index_col=0)
    #
    # df3 = recipepp.concat_data(df1,df2)
    # cat4_df = pd.read_csv('crawl_data/id_4category.csv',index_col=0)
    # print(df3.shape,len(df3))
    # recipepp.save_data('recipe_info',df3)
    #
    # df4 = recipepp.merge_data(cat4_df,df3)
    # print(df4.shape,len(df4))
    # recipepp.save_data('recipe_data_final',df4)

    df = pd.read_csv('crawl_data/recipe_data_final_0_135326.csv',index_col=0)
    # print(df.columns)
    '''
    Index(['id', 'cat1', 'cat2', 'cat3', 'cat4', 'recipe_id', 'rec_title',
       'rec_sub', 'rec_source', 'rec_step', 'rec_tag'],
      dtype='object')
    '''
    # for x in range(6,11):
    #     print(sum(df.iloc[:,x] == '-'))
    '''
    315
    307
    9747
    11057
    135318
    8
    '''
    print(sum(df['rec_tag'] != '-'))
    print(df.loc[df['rec_tag'] != '-','rec_tag'])
    # 결측치 제거
    df2 = df.iloc[:,:10]

    df_dropna = df2.dropna(axis=0) #(125964, 10)
    df_dropna = df_dropna.drop(columns=['recipe_id'])
    df_dropna.to_csv('crawl_data/recipe_data_dropna.csv',encoding='utf-8',index=False)
