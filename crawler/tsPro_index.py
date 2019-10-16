#enconding=utf-8
## 计算大盘各类指数的指标
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')

index=["000001.sh","399001.sz","000300.sh","000905.sh"]
def get_trade_vol(index_name,start_date,end_date):
    df= pro.index_daily(index_name, start_date, end_date)[["ts_code","vol","amount"]]
    df["amount"]=round(df["amount"]/100000,2)
    return df
def get_trade_margin(exchange_id=None,start_date='20190901',end_date='20190910'):
    df = pro.margin(exchange_id=exchange_id,start_date=start_date,end_date=end_date)
    df["margin_amount"]=round(df["rzrqye"]/100000000,2)
    return df
if __name__ == '__main__':
    start_date='20190901'
    end_date='20190910'
    df=get_trade_margin(exchange_id=None,start_date=start_date,end_date=end_date)
    print(df.head())

