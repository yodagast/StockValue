### 龙头股息策略
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
pd.set_option('display.max_colwidth',500)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr',False)

def baseStockSelector(date=get_recent_date()):
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')
    df = pro.daily_basic(ts_code='', trade_date=date)
    return pd.merge(data, df, on='ts_code')

def industrySelector(top=True,k=1e+8,date=get_recent_date()):
    data = baseStockSelector(date)
    industry=data.groupby(["industry"]).agg({"total_mv":"sum"}).reset_index().sort_values(by="total_mv",ascending=False)
    industry.columns=["industry","industry_mv"]
    if(top):
        industry = industry[industry.industry_mv > k]
    else:
        industry=industry[industry.industry_mv<k]
    #logger.info(industry["industry"])
    return pd.merge(data, industry, on='industry')

def turnoverSelector(ts_code,start_date,end_date):
    return

def topStockSelector(top_k=5,top_col='total_mv',df=industrySelector()):
    df.sort_values(['industry', top_col], ascending=[1, 0], inplace=True)
    df = df.groupby(['industry']).head(top_k).reset_index()
    return df
def turnover_stockSelector(ts_code,start_date,end_date):
    df_basic = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date)
    df_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    flow_cols = df_daily.columns.difference(df_basic.columns)
    df = pd.merge(df_basic, df_daily[flow_cols], left_index=True, right_index=True, how='inner')
    cond=(df["pct_chg"].abs()>2) &(df["turnover_rate_f"]>0.3) & (df["turnover_rate_f"]<3)
    return df[cond]

if __name__ == '__main__':
    df= industrySelector(top=True,k=1e+8,date="20200313").dropna()
    columns=["ts_code","name","industry","trade_date","close","turnover_rate_f","dv_ttm","dv_ratio","pe_ttm"]
    df=topStockSelector(top_k=6,df=df)
    condition=(df["turnover_rate_f"]>0.3) & (df["turnover_rate_f"]<3) & (df["pe_ttm"]<40) & (df["dv_ratio"]>2.5)
    df=df[columns][condition]
    ts_code=df["ts_code"].values[:100]
    tmp=turnover_stockSelector(ts_code=",".join(ts_code),start_date="20200301",end_date=get_recent_date())
    columns.extend(["change", "high", "low", "open", "pct_chg", "pre_close"])
    tmp=pd.merge(tmp, df)[columns]
    print(tmp)


