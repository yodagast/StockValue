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
df=pro.query('stock_basic', exchange='',is_hs='H',
             list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(df.shape)
#ts.set_token('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')
