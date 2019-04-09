from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import get_codelist,is_SH
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')
df=pro.query('stock_basic', exchange='',is_hs='H',
             list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(df.shape)

def get_recent_date():
    yesterday = datetime.now() - timedelta(1)
    yesterday = yesterday.strftime("%Y%m%d")
    today = time.strftime("%Y%m%d", time.localtime())
    return yesterday

def get_moneyflow(ts_code):
    df=pro.moneyflow(ts_code=ts_code,trade_date=get_recent_date())
    df["buy_vol"]=df["buy_sm_vol"]+df["buy_md_vol"]+df["buy_lg_vol"]+df["buy_elg_vol"]
    df["buy_amount"]=df["buy_sm_amount"]+df["buy_md_amount"]+df["buy_lg_amount"]+df["buy_elg_amount"]
    df["sell_vol"]=df["sell_sm_vol"]+df["sell_md_vol"]+df["sell_lg_vol"]+df["sell_elg_vol"]
    df["sell_amount"]=df["sell_sm_amount"]+df["sell_md_amount"]+df["sell_lg_amount"]+df["sell_elg_amount"]
    return df[["buy_vol","sell_vol","buy_amount","sell_amount"]]

for code in get_codelist():
    df=get_moneyflow(is_SH(code))
    logger.info("{0} df shape {1}  : {2}".format(is_SH(code),df.shape,df.values.tolist()))

