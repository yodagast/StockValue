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
pro=ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')

def get_fund_basic(cols=["ts_code","name","issue_amount","invest_type"],amount=20.0):
    df = pro.fund_basic(market='E')
    cond=(df.delist_date.isnull()) #& (df.issue_amount>amount)
    if ((cols == None) | (len(cols) < 1)):
        cols = df.columns
    df=df[cond][cols]
    return df

get_fund_basic()