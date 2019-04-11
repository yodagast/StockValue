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
def main():
    dates=get_cal_date()
    today = datetime.now()
    if(today.hour<19):
        today = today - timedelta(1)
    end_date = today.strftime("%Y%m%d")
    last_year= datetime.now() - timedelta(365)
    start_date = last_year.strftime("%Y%m%d")
    codes=list(map(is_SH,get_list()))
    for code in codes:
        df=pro.daily(ts_code='000001.SZ', start_date=start_date, end_date=end_date)



