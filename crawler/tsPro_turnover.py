from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')
df = pro.daily_basic(ts_code='600036.SH', trade_date='20190404',
                     fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe_ttm,pb,ps_ttm')

def get_stock_feature(date,ts_code='600036.SH'):
    df_basic=pro.daily_basic(ts_code=ts_code, trade_date=date,
                     fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe_ttm,pb,ps_ttm')
    df_flow=pro.moneyflow(ts_code=ts_code,start_date=date, end_date=date)
    df_daily= pro.daily(ts_code=ts_code, start_date=date, end_date=date)
    return pd.concat([df_basic, df_flow,df_daily], axis=1)


def get_daily_feature(date="",ts_code=""):
    res=pd.DataFrame()
    if(isinstance(ts_code,str)):
        res=get_stock_feature(date,ts_code)
    elif(isinstance(ts_code,list)):
        for code in ts_code:
            tmp=get_stock_feature(date,ts_code)
            res = res.append(tmp, ignore_index=True)
    return res


print(df)