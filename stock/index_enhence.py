from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,configparser
import talib as ta
from urllib.parse import urlencode
from crawler.util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
pd.set_option('display.max_colwidth',500)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr',False)
def get_codes():
    config = configparser.ConfigParser()
    config.read("./config.cfg")
    sw_idx = config.get("SW", "SI").split(",")
    df=pro.index_member(index_code=sw_idx)
    codes = ",".join(df["con_code"].to_list())
    df = pro.bak_daily(ts_code=codes, start_date='20180101', end_date='20181011')
    print(df)

get_codes()