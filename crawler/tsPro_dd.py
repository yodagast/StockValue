from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')
df=pro.query('stock_basic', exchange='',is_hs='H',
             list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(df.shape)

def get_recent_date():
    today = datetime.now()
    if (today.hour < 19):
        today = today - timedelta(1)
    return today.strftime("%Y%m%d")

def get_moneyflow(ts_code):
    df=pro.moneyflow(ts_code=ts_code,trade_date=get_recent_date())
    df["dd_buy_vol"]=df["buy_md_vol"]+df["buy_lg_vol"]+df["buy_elg_vol"]#df["buy_sm_vol"]+
    df["dd_buy_amount"]=df["buy_md_amount"]+df["buy_lg_amount"]+df["buy_elg_amount"]#df["buy_sm_amount"]+
    df["dd_sell_vol"]=df["sell_md_vol"]+df["sell_lg_vol"]+df["sell_elg_vol"]#df["sell_sm_vol"]+
    df["dd_sell_amount"]=df["sell_md_amount"]+df["sell_lg_amount"]+df["sell_elg_amount"]#df["sell_sm_amount"]+
    return df[["dd_buy_vol","dd_sell_vol","net_mf_vol","net_mf_amount"]]

for code in get_list():
    df=get_moneyflow(is_SH(code))
    mydict = {c: df[c][0] for c in df.columns}
    logger.info("{0} dd : {1}".format(get_codeName(is_SH(code)),mydict))

