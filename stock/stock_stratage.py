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
import pyarrow as pa
import pyarrow.parquet as  pq
from urllib.parse import urlencode
from crawler.util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
ts.set_token('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
pd.set_option('display.max_colwidth',500)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr',False)

def ts_daily_data(path='./',start_date='202001010',end_date='20200331'):
    df = pro.trade_cal(exchange='SSE', start_date=start_date, end_date=end_date)
    df = df[df["is_open"] == 1]
    for idx, dat in df.iterrows():
        tmp = pro.query('daily_basic', ts_code='',trade_date=dat['cal_date'])
        table = pa.Table.from_pandas(tmp)
        if (table != None):
            pq.write_to_dataset(table, root_path=path + "{}_{}.parquet".format(start_date, end_date))
            time.sleep(20)
    logger.info(df.columns)

def data_selector():
    df=pd.read_parquet(path="./20200101_20200608.parquet")
    core_codes = ["300498.SZ", "000002.SZ", "600104.SH", "601166.SH","601601.SH","601318.SH"]
    res=pd.DataFrame()
    for code in core_codes:
        res=res.append(df[df["ts_code"]==code].sort_values(by=['trade_date']))
    print(res.head())
    print(res.columns)
    return res
if __name__ == '__main__':
    data_selector()




