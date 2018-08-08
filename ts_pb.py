import os,sys
import tushare as ts
import pandas as pd
import numpy as np
def get_basic():
    '''
    获取stock基本情况，pb，pe
    :return:
    '''
    df = ts.get_stock_basics()
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
        cond = (df.industry == ind) & (df.pb > 0.0) & (df.pb < 1.2) & (df.pe > 0.1) & (df.pe < 20.0)
        bank = df[["name", "industry", "pe", "pb", "fixedAssets",]][cond].sort_values(by="pe")
        tmp = bank.head(100)
        res = pd.concat([res, tmp])
        res.to_csv("pb.csv",sep="\t")
    return  res
get_basic()