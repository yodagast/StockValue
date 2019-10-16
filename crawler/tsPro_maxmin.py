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

def get_week_maxmin(ts_code,start_date,end_date):
    '''获取code交易的日线、周线 月线行情
    :param ts_code:
    :param start_date:
    :param end_date:
    :return:
    '''
    df = pro.weekly(ts_code=ts_code,start_date=start_date, end_date=end_date, fields='ts_code,trade_date,open,high,low,close,vol,amount')
    return df[["high","low"]].max(axis=0)
     #TODO
def get_day_maxmin(ts_code,start_date,end_date):
    '''获取code交易的日线、周线 月线行情
    :param ts_code:
    :param start_date:
    :param end_date:
    :return:
    '''

    df = pro.daily(start_date=start_date, end_date=end_date, fields='ts_code,trade_date,open,high,low,close,vol,amount')
    #TODO
    return df[["high", "low"]].max(axis=0)

