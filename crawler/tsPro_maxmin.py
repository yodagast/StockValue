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
pro=ts.pro_api('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')

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

if __name__ == '__main__':
    end_date=get_recent_date()
    start_date=get_start_date()
    print(end_date,start_date)
    df=get_week_maxmin(["000002.sz","600026.sh"],start_date,end_date)
    print(df)
    df = get_maxmin(["000002.sz", "600026.sh"],"weekly", start_date, end_date)
    print(df)
