from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

#pro = ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
pd.set_option('display.max_colwidth',500)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr',False)
def get_recent_date(isString=True):
    today = datetime.now()
    if (today.hour < 19):
        today = today - timedelta(1)
    if(isString):
        return today.strftime("%Y%m%d")
    return today


def get_freq_vol_stat(codes,start_date,end_date):
    res = pd.DataFrame()
    for ts_code in codes:
        df = ts.pro_bar(ts_code=ts_code,freq='min', start_date=start_date,end_date=end_date)
        df["amount"] = df["amount"] / 1000
        logger.info("processing :{0} ".format(ts_code))
        print(df)
        res = res.append(df, ignore_index=True)
    return res

def main():
    ts.set_token('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
    #pro = ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
    #today = get_recent_date()
    end_date = get_recent_date()
    last_year= datetime.now() - timedelta(1)
    start_date = last_year.strftime("%Y%m%d")
    mycodes = ["600308.SH"]#,"600302.SH","600612.SH","600887.SH"]
    #mycodes=["000002.SZ","600027.SH","600867.SH","000963.SZ","600660.SH"
    #    ,"601318.SH","600036.SH","601166.SH","601601.SH"]
    df=get_freq_vol_stat(mycodes,start_date, end_date)
    tmp=df[df["ts_code"]=='000002.SZ']

main()