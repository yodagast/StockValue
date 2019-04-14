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

def get_moneyflow(ts_code,start_date,end_date):
    df=pro.moneyflow(ts_code=ts_code,start_date=start_date,end_date=end_date)
    df["dd_buy_vol"]=df["buy_md_vol"]+df["buy_lg_vol"]+df["buy_elg_vol"]#df["buy_sm_vol"]+
    df["dd_buy_amount"]=df["buy_md_amount"]+df["buy_lg_amount"]+df["buy_elg_amount"]#df["buy_sm_amount"]+
    df["dd_sell_vol"]=df["sell_md_vol"]+df["sell_lg_vol"]+df["sell_elg_vol"]#df["sell_sm_vol"]+
    df["dd_sell_amount"]=df["sell_md_amount"]+df["sell_lg_amount"]+df["sell_elg_amount"]#df["sell_sm_amount"]+
    return df[["dd_buy_vol","dd_sell_vol"]]

def get_single_code_df(ts_code,start_date,end_date):
    df_basic = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date)
    df_flow = pro.moneyflow(ts_code=ts_code, start_date=start_date, end_date=end_date)
    df_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    flow_cols = df_flow.columns.difference(df_basic.columns)
    df = pd.merge(df_basic, df_flow[flow_cols], left_index=True, right_index=True, how='outer')
    daily_cols = df_daily.columns.difference(df.columns)
    df = pd.merge(df, df_daily[daily_cols], left_index=True, right_index=True, how='outer')
    df_flow=get_moneyflow(ts_code,start_date,end_date)
    flow_cols = df_flow.columns.difference(df.columns)
    df = pd.merge(df, df_flow[flow_cols], left_index=True, right_index=True, how='outer')
    return df

def get_lastyear_stat(codes,start_date,end_date):
    res = pd.DataFrame()
    for ts_code in codes:
        #print(ts_code)
        df = get_single_code_df(ts_code, start_date, end_date)
        name = get_codeName(ts_code)
        df["code_name"] = name
        logger.info("processing :{0} {1}".format(ts_code, name))
        res = res.append(df, ignore_index=True)
    return res


def main():
    dates=get_cal_date()
    #today = get_recent_date()
    end_date = get_recent_date()
    last_year= datetime.now() - timedelta(365)
    start_date = last_year.strftime("%Y%m%d")
    mycodes=get_ts_codes()
    df=get_lastyear_stat(mycodes,start_date,end_date)
    df.to_csv("../stock/{0}-lastyear-mystock.csv".format(end_date), sep="\t", index=False)
    fullcodes=get_full_ts_codes()
    df=get_lastyear_stat(fullcodes, start_date, end_date)
    df.to_csv("../stock/{0}-lastyear-fullstock.csv".format(end_date), sep="\t", index=False)

main()



