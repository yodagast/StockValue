from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import get_codelist
from util import *

logging.basicConfig(level=logging.INFO, format=' %(message)s ')
logger = logging.getLogger(__name__)
pro=ts.pro_api('ec128793ed40d17b0654785138fd519fc1f1ffede1e89e5701f752ed')
#df = pro.daily_basic(ts_code='600036.SH', trade_date='20190404',
#                     fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe_ttm,pb,ps_ttm')

def get_stock_feature(date,ts_code='600036.SH'):
    logger.info("prepare to caculate {0}:".format(ts_code))
    df_basic=pro.daily_basic(ts_code=ts_code, start_date=date, end_date=date,
                     fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe_ttm,pb,ps_ttm')
    df_flow=pro.moneyflow(ts_code=ts_code,start_date=date, end_date=date)
    df_daily= pro.daily(ts_code=ts_code, start_date=date, end_date=date)
    flow_cols =df_flow.columns.difference(df_flow.columns)
    df=pd.merge(df_basic, df_flow[flow_cols],left_index=True, right_index=True, how='outer')
    daily_cols = df_daily.columns.difference(df.columns)
    df=pd.merge(df, df_daily[daily_cols],left_index=True, right_index=True, how='outer')
    df["amp"]=round((df["high"]-df["low"])/df["pre_close"],3)
    df["tomorrow_high"]=round((df["amp"]+1)*df["close"],4)
    df["tomorrow_low"]=round((1-df["amp"])*df["close"],4)
    df["name"]=get_codeName(ts_code)
    tmp=df[["tomorrow_high","tomorrow_low","close","name","pe_ttm","turnover_rate_f","amp"]]
    mydict={c:tmp[c][0] for c in tmp.columns}
    #logger.info("{1}:next-high-low:{4}-{5},close:{6},turnover_rate(f):{2},amplitude:{3}".
    #            format(date,ts_code,df["turnover_rate_f"][0],df["amp"][0],df["tomorrow_high"][0],df["tomorrow_low"][0],df["close"][0]))
    logger.info("{0}-{1}".format(date,mydict))
    return tmp


def get_daily_feature(date,ts_code="600036.SH"):
    res=pd.DataFrame()
    if(isinstance(ts_code,str)):
        res=get_stock_feature(date,ts_code)
    elif(isinstance(ts_code,list)):
        for code in ts_code:
            tmp=get_stock_feature(date,code)
            res = res.append(tmp, ignore_index=True)
    return res

def main():
    #yesterday = datetime.now() - timedelta(1)
    #yesterday = yesterday.strftime("%Y%m%d")
    today = datetime.now()
    if (today.hour < 19):
        today = today - timedelta(1)
    today=today.strftime("%Y%m%d")
    industry = [  # ["银行", ],
        # ["化学制药", "生物制药", "中成药"],
        # ["汽车配件", "汽车整车", "纺织机械"],
        ["造纸", "水泥", "空运"],
        # ["建筑施工", "环境保护", ],
        # ["白酒", "乳制品"],
        # ["煤炭开采", "石油加工", "石油开采"],
        # ["特种钢", "矿物制品", "普钢"],
        # ["火力发电", "新型电力", "水利发电"],
        # ["家用电器", "电器仪表", "化工原料"],
        # ["医药商业", "医疗保健", "超市连锁"],
        # ["全国地产", "区域地产"],
        ["证券", "保险"]]
    flatten_list = lambda l: [item for sublist in l for item in sublist]
    if (isinstance(industry[0], list)):
        full_list = get_codelist(flatten_list(industry))
        if (str(full_list[0]).find("S") < 0):
            full_list = list(map(is_SH, full_list))
    mylist = list(map(is_SH, get_list()))
    df = get_daily_feature(today, mylist)
    if (os.path.exists("../stock") == False):
        os.mkdir("../stock")
    df.to_csv("../stock/{0}-mystock.csv".format(today), sep="\t", index=False)
    df = get_daily_feature(today, full_list)
    df.to_csv("../stock/{0}-full-stock.csv".format(today), sep="\t", index=False)

main()