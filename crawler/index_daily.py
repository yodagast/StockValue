from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')

def get_daily_index(index_name="SSE"):
    end_date = get_recent_date()
    last_year = datetime.now() - timedelta(30)
    start_date = last_year.strftime("%Y%m%d")
    if(index_name=="SSE"):
        logger.info("get shanghai stock index")
        df = pro.index_daily(ts_code='000001.SH', start_date=start_date, end_date=end_date)
    else:
        logger.info("get {} stock index".format(index_name))
        return
    df["vol"] = round(df["vol"] / 10000, 2)
    df["amount"]=round(df["amount"]/100000,2)
    print(df)

get_daily_index()