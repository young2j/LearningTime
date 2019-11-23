import tushare as ts
import pandas as pd
# from functools import reduce

start='2013-07-31'
end='2018-07-31'
path="/home/hadoop/eclipse-workspace/FinancialRiskEval/data/"

# def get_hs300(start,end,path):
#     codes = ts.get_hs300s().code
#     k = []
#     for code in codes:
#         k_data = ts.get_k_data(code=code,start='2013-07-31',end='2018-07-31')
#         k.append(k_data)
#     concat = lambda x,y:pd.concat([x,y],axis=0)
#     hs300 = reduce(concat,k)
#     hs300_mean = hs300.groupby('date').mean()
#     return hs300_mean.to_csv(path)

def get_hs300(start,end,path):
    codes = ts.get_hs300s().code
    for code in codes:
        k_data = ts.get_k_data(code=code,start='2013-07-31',end='2018-07-31')
        k_data.to_csv(path+"hs300/"+code+".csv")

def get_index(start,end,path):
    index_dict = {'上证综指':'000001','深证成指':'399001','国债指数':'000012'}
    for code in index_dict.values():
        index_data = ts.get_k_data(code=code,start=start,end=end,index=True)
        index_data.to_csv(path+"hsindex/"+code+".csv")
        
# def get_gdp():
#     gdp = ts.get_gdp_quarter()
#     from math import modf
#     index = gdp.iloc[:,0].apply(modf).map(lambda x: \
#             str(int(x[1]))+'-'+str(int(round(x[0],1)*10)))
#     gdp.index = pd.to_datetime(index)
#     gdp = gdp.resample(rule='D').ffill()
#     gdp = gdp.drop(['quarter'],axis=1).reset_index()
#     return gdp.to_csv(path+"gdp.csv")

if __name__=="__main__":
    print("开始下载沪深300成分股数据...")
    try:
        get_hs300(start=start,end=end,path=path)
        print("已下载沪深300成分股交易数据至%s hs300/" % path)
    except Exception as e:
        raise e
    
    print("开始下载市场指数数据...")
    try:
        get_index(start=start,end=end,path=path)
        print("已下载上证综指数据至%s" % (path + "hsindex/" + "000001.csv"))
        print("已下载深证成指数据至%s" % (path + "hsindex/" + "399001.csv"))
        print("已下载国债指数数据至%s" % (path + "hsindex/" + "000012.csv"))
    except Exception as e:
        raise e
     
#     print("开始下载GDP数据...")
#     get_gdp()
#     print("已下载GDP数据至%s gdp.csv"% path)