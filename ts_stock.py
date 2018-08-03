import os,sys
import tushare as ts
import pandas as pd
import numpy as np
#report=ts.get_report_data(2018,1)
#growth_data=ts.get_growth_data(2014,3)
#debtpaying=ts.get_debtpaying_data(2014,3)
#cashflow=ts.get_cashflow_data(2014,3)

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
        cond = (df.industry == ind) & (df.pb > 0.0) & (df.pb < 1.2) & (df.pb > 0.1) & (df.pe < 50.0)
        bank = df[["name", "industry", "pe", "pb", "fixedAssets",]][cond].sort_values(by="pe")
        tmp = bank.head(100)
        res = pd.concat([res, tmp])
        res.to_csv("res.csv",sep="\t")
    return  res

def get_profit(year=2017,quarter=4):
    file_name="./data/profit_{}_{}.tsv".format(year,quarter)
    if (os.path.exists(file_name)):
        profit=pd.read_csv(file_name,sep="\t",dtype={'code':'object'})
    else:
        profit = ts.get_profit_data(year, quarter)
        profit.to_csv(file_name,sep="\t",index=False)
    cond = (profit.roe>8.0)# & (profit.profits>1.0)
    res=profit[["code","net_profits","roe"]][cond].sort_values(by="roe")
    return res

def get_growth(year=2018,quarter=1):
    df = ts.get_growth_data(year, quarter)
    cond = (df.mbrg > 5.0) & (df.nprg > 2.0)
    res = df[["mbrg", "nprg", ]][cond].sort_values(by="mbrg")
    return res

def get_em(df):
    '''
    计算获得权益乘数，越大表示公司的负债越高
    :return:
    '''
    df["em"]=df["roe"]/df["npr"]/(df["business_income"]/df["totalAssets"])
    return df

def get_basic_stock():
    basic = get_basic()
    profit = get_profit()
    res = basic.merge(profit, left_on='code', right_on='code')
    res["roa"] = res["net_profits"] / res["fixedAssets"] * 100
    columns = ['net_profits', 'fixedAssets', ]
    res.drop(columns, inplace=True, axis=1)
    res = res.round({"roa": 3, })
    res.sort_values(by="roa", ascending=False).to_csv("basic_profit.tsv", sep="\t")
    print(res.head(50))

get_basic_stock()