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
def get_full_ts_codes(isPro=True):
    industry = [  # ["银行", ],
        # ["化学制药", "生物制药", "中成药"],
         ["汽车配件", "汽车整车", "纺织机械"],
        ["造纸", "水泥", "空运"],
        # ["建筑施工", "环境保护", ],
        # ["白酒", "乳制品"],
        # ["煤炭开采", "石油加工", "石油开采"],
        # ["特种钢", "矿物制品", "普钢"],
        # ["火力发电", "新型电力", "水利发电"],
        # ["家用电器", "电器仪表", "化工原料"],
        # ["医药商业", "医疗保健", "超市连锁"],
        # ["全国地产", "区域地产"],
        ["证券", "保险"]]
    flatten_list = lambda l: [item for sublist in l for item in sublist]
    codes = get_codelist(flatten_list(industry),isPro)
    return codes
def get_codelist( industry="银行",isPro=True):
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
    if(isPro):
        res=list(map(is_SH,res))
    return res

def get_codeName(ts_code):
    '''
    :param ts_code:给定股票代码，返回股票名称
    :return:
    '''
    pro = ts.pro_api()
    df = pro.namechange(ts_code=ts_code, fields='ts_code,name,start_date,end_date,change_reason')
    if(df.shape[1]>0):
        res= df["name"][0]
    else:
        res= "ERROR"

    logger.info("get code {0} name: {1}".format(ts_code,res))
    return res

def get_ts_codes(isPro=True):
    my_list=["600585","600036","600660","000002","600062","600867","603337",
             "600308","600703","601288","601939","002294","002310"]
    candidate=["600703","002624","002008","002001","600104","000826",
               "000538","000338","000501"]
    my_list.extend(candidate)
    if(isPro):
        return list(map(is_SH,my_list))
    return my_list

def get_lastyear_date(today=None,lastyear=365,isPro=True):
    if(today==None):
        today = date.today()
    my_days=[]
    for i in range(lastyear,0,-1):
        yesterday = today - timedelta(days=i)
        if(isPro):
            my_days.append(yesterday.strftime("%Y%m%d"))
        else:
            my_days.append(yesterday.strftime("%Y-%m-%d"))
    return my_days

def get_recent_date():
    today = datetime.now()
    if (today.hour < 19):
        today = today - timedelta(1)
    return today.strftime("%Y%m%d")

def get_cal_date(start_date=None,end_date=None,during=365,isPro=True):
    if(end_date==None):
        end_date=date.today()
    if(start_date==None):
        #start_date=end_date+relativedelta(months=-12)
        start_date=end_date- timedelta(days=during)
    if(isPro==True):
        end_date = end_date.strftime("%Y%m%d")
        start_date = start_date.strftime("%Y%m%d")
    else:
        end_date = end_date.strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
    pro = ts.pro_api()
    df=pro.trade_cal(start_date=start_date,end_date=end_date)
    #df[["exchange", "cal_date"]][df["is_open"] == 1]
    return  df[ "cal_date"][df["is_open"] == 1].to_list()

def is_cal_date(date=None):
    pro = ts.pro_api()
    df = pro.trade_cal(start_date=date, end_date=date)
    if( df.empty | df["is_open"][0] == 0):
        return False
    return True






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


