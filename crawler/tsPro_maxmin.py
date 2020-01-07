from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')

def get_maxmin(ts_code,func,start_date,end_date):
    '''获取code周线的最大最小值
    :param ts_code: str or List
    :func 使用weekly、daily、
    :param start_date:
    :param end_date:
    :return:
    '''
    if(func=="weekly"):
        func=pro.weekly
    elif(func=="daily"):
        func=pro.daily
    elif(func=="monthly"):
        func=pro.monthly
    else:
        logger.error("function not fund")
    res=pd.DataFrame()
    if(isinstance(ts_code,str)):
        df = func(ts_code=ts_code,start_date=start_date, end_date=end_date)
        s = df[["ts_code", "high", "low"]].max(axis=0)
        logger.info(s.values)
        res=res.append(s,ignore_index=True)
    elif(isinstance(ts_code,list)):
        for code in ts_code:
            df = func(ts_code=code, start_date=start_date, end_date=end_date)
            s = df[["ts_code", "high", "low"]].max(axis=0)
            logger.info(s.values)
            res = res.append(s, ignore_index=True)
    else:
        logger.error("ts_code TYPE ERROR")
    return res

def get_week_maxmin(ts_code,start_date,end_date):
    '''获取code周线的最大最小值
    :param ts_code: str or List
    :param start_date:
    :param end_date:
    :return:
    '''
    return get_maxmin(ts_code,"weekly",start_date,end_date)
def get_day_maxmin(ts_code,start_date,end_date):
    '''获取code交易的日线、周线 月线行情
    :param ts_code:
    :param start_date:
    :param end_date:
    :return:
    '''
    return get_maxmin(ts_code, "daily", start_date, end_date)

def get_month_maxmin(ts_code,start_date,end_date):
    '''获取code交易的日线、周线 月线行情
    :param ts_code:
    :param start_date:
    :param end_date:
    :return:
    '''
    return get_maxmin(ts_code, "monthly", start_date, end_date)

if __name__ == '__main__':
    end_date=get_recent_date()
    start_date=get_start_date()
    code_list=["600027"]#get_ts_codes()
    logger.info("computing weekly price from {} to {}".format(start_date,end_date))
    #df=get_week_maxmin(["000002.sz","600660.sh"],start_date,end_date)
    #print(df)
    start_date = get_start_date(during=120)
    logger.info("computing monthly price from {} to {}".format(start_date, end_date))
    df = get_day_maxmin(["600027.sh", "600660.sh"], start_date, end_date)
    df = get_maxmin(["600027.sh", "600660.sh"],"monthly", start_date, end_date)
    print(df)
