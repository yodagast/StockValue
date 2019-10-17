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
    return df.sort_values(by=["exchange_id","trade_date"])

def get_trade_hsgt(start_date='20190901',end_date='20190910'):
    df= pro.moneyflow_hsgt(start_date=start_date, end_date=end_date)
    df["hgt"]=round(df["hgt"]/100,2)
    df["sgt"]=round(df["sgt"]/100,2)
    df["south_money"]=round(df["south_money"]/100,2)
    return df

if __name__ == '__main__':
    start_date='20191008'
    end_date=get_recent_date()
    df=get_trade_margin(exchange_id=None,start_date=start_date,end_date=end_date)
    print(df.head(60))

