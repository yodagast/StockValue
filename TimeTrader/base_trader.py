from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
import talib as ta
from urllib.parse import urlencode
from crawler.util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
pd.set_option('display.max_colwidth',500)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr',False)

def tushare_data(ts_code="600027.SZ",sdate="20200101",edate="20200930",freq="5min"):
    df = ts.pro_bar(ts_code, adj='qfq', freq=freq,start_date=sdate, end_date=edate).sort_values(by=["trade_time"],ascending=True)
    df["label"]=(df["close"]-df["close"].shift(1,fill_value=0))
    df.drop(df.index[0],inplace=True)
    return df

def



