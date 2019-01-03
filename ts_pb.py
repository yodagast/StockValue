import os,sys
import tushare as ts
import pandas as pd
import numpy as np

def get_basic(yesterday=None):
    '''
    获取stock基本情况，pb，pe
    :return:
    '''
    if(yesterday==None):
        df = ts.get_stock_basics()
    else:
        df=ts.get_stock_basics(yesterday)
    industry = pd.unique(df["industry"])
    if (os.path.exists("industry.csv") == False):
        f = open("industry.csv", "w")
        for d in industry:
            f.write(d + "\n")
        f.close()
    if (os.path.exists("col.csv") == False):
        f = open("col.csv", "w")
        for col in df.columns:
            f.write(col + "\n")
        f.close()
    res = pd.DataFrame()
    for ind in industry:
        #if((str(ind).find("医")<0) & (str(ind).find("药")<0)):
        #    continue
        cond = (df.industry == ind) & (df.pb > 0.0) & (df.pb < 1.01) & (df.pe > 0.1) & (df.pe < 30.0)
        bank = df[["name", "industry", "pe", "pb", "fixedAssets",]][cond].sort_values(by="pe")
        tmp = bank.head(100)
        res = pd.concat([res, tmp])
        res.to_csv("pb.csv",sep="\t")
    return  res

date="2018-10-22"
res2=get_basic(date)[["name","industry"]]
res1=get_basic("2018-10-23")[["name","industry"]]
print(res1.shape)
print(res2.shape)
new_pb=res2.append(res1).drop_duplicates(keep=False)
new_pb.to_csv("new_pb.csv",sep="\t")
print(new_pb.shape)