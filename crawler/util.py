from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_SH(x):
    '''
    :param x:给定6位代码，返回代码.SZ/SH
    :return:
    '''
    if(str(x).startswith("6")):
        return x+".SH"
    else:
        return x+".SZ"

def get_codelist( industry="银行"):
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
    res=list(map(is_SH,res))
    return res

def get_codeName(ts_code):
    '''
    :param ts_code:给定股票代码，返回股票名称
    :return:
    '''
    pro = ts.pro_api()
    df = pro.namechange(ts_code=ts_code, fields='ts_code,name,start_date,end_date,change_reason')
    return df["name"][0]

def get_list():
    my_list=["600585","600036","600660","000002","600062","600867","600337",
             "600308","600703","601288","601939","002294","002310"]
    candidate=["600703","002624","002008","002001","600104","000826","000501"]
    my_list.extend(candidate)
    return my_list

def get_lastyear_date(today=None,lastyear=365):
    if(today==None):
        today = date.today()
    my_days=[]
    for i in range(lastyear,0,-1):
        yesterday = today - timedelta(days=i)
        my_days.append(yesterday.strftime("%Y%m%d"))
    return my_days

def get_cal_date(start_date=None,end_date=None,during=365):
    if(end_date==None):
        end_date=date.today()
    if(start_date==None):
        #start_date=end_date+relativedelta(months=-12)
        start_date=end_date- timedelta(days=during)
        end_date = end_date.strftime("%Y%m%d")
        start_date = start_date.strftime("%Y%m%d")
    pro = ts.pro_api()
    df=pro.trade_cal(start_date=start_date,end_date=end_date)
    #df[["exchange", "cal_date"]][df["is_open"] == 1]
    return  df[ "cal_date"][df["is_open"] == 1].to_list()





class Version(object):
    @staticmethod
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


