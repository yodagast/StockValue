from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform

def get_code_list():
    return ["600036","600585","600028","601939","600308","159938"]
def get_huge_sale(code,date=None):
    date = time.strftime("%Y-%m-%d", time.localtime())
    d=time.strftime("%Y:%m:%d", time.localtime())
    tmp=ts.get_sina_dd(code,vol=500,date=date)
    time.sleep(5)
    res=tmp.groupby(tmp["code","name","volume"])["volume"].sum()
    return res

def get_huge_exchage(code_list=None,date=None):
    if(code_list==None):
        code_list=get_code_list()
    date = time.strftime("%Y-%m-%d", time.localtime())
    df=pd.DataFrame()
    for code in code_list:
        tmp=ts.get_sina_dd(code,vol=500,date=date)
        df=df.append(tmp,ignore_index=True)
    df["code"]=df["code"].apply(str)
    df["name"]=df["name"].apply(str)
    df["type"]=df["type"].apply(str)
    df["volume"] = df["volume"].apply(int)
    print(df.head(2))
    tmp1=df.groupby(['name',"type"])["volume"].sum()
    tmp=pd.DataFrame(tmp1).reset_index()
    print(type(tmp))
    return tmp


def mychoice():
    yiyao_list = ["600062", "600079", "600196", "600056", "603579", "000423", "600216", "600867", "601607", "000999"]
    list = yiyao_list
    return list


def get_codelist(industry="银行"):
    '''
    给定行业类型，获取所有该行业的公司股票代码
    :param industry: string or list
    :return:
    '''
    df = ts.get_stock_basics()
    res = []
    if (isinstance(industry, str)):
        tmp = df[["name", "industry", "pe", "pb", ]][(df.industry == industry)]
        return tmp.index.tolist()
        # cond = (df.industry == industry)# & (df.pb > 0.0) & (df.pb < 1.01) & (df.pe > 0.1) & (df.pe < 30.0)
    elif (isinstance(industry, list)):
        for ind in industry:
            tmp = df[["name", "industry", "pe", "pb", ]][(df.industry == ind)]
            tmp_list = tmp.index.tolist()
            res.extend(tmp_list)
    return res


def main():
    date = time.strftime("%Y-%m-%d", time.localtime())
    industry = [["银行", ],
                ["化学制药", "生物制药", "中成药"],
                ["汽车配件", "汽车整车", "纺织机械"],
                ["造纸", "水泥", "空运"],
                ["建筑施工", "环境保护", ],
                ["白酒", "乳制品"],
                ["煤炭开采", "石油加工", "石油开采"],
                ["特种钢", "矿物制品", "普钢"],
                ["火力发电", "新型电力", "水利发电"],
                ["家用电器", "电器仪表", "化工原料"],
                ["医药商业", "医疗保健", "超市连锁"],
                ["全国地产", "区域地产"],
                ["证券", "保险"]]
    list=get_codelist()
    df=get_huge_exchage(list)
    df.to_csv("../data/{}/huge-exchage.csv".format(date),index=False)


main()
