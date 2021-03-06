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
    logger.info("prepare to caculate {0} on {1}".format(ts_code,date))
    df_basic=pro.daily_basic(ts_code=ts_code, start_date=date, end_date=date,
                     fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe_ttm,pb,ps_ttm')
    df_flow=pro.moneyflow(ts_code=ts_code,start_date=date, end_date=date)
    df_daily= pro.daily(ts_code=ts_code, start_date=date, end_date=date)
    flow_cols =df_flow.columns.difference(df_basic.columns)
    df=pd.merge(df_basic, df_flow[flow_cols],left_index=True, right_index=True, how='outer')
    daily_cols = df_daily.columns.difference(df.columns)
    df=pd.merge(df, df_daily[daily_cols],left_index=True, right_index=True, how='outer')
    df["amp"]=round((df["high"]-df["low"])/df["pre_close"],3)
    df["tomorrow_high"]=round((df["amp"]+1)*df["close"],4)
    df["tomorrow_low"]=round((1-df["amp"])*df["close"],4)
    df["name"]=get_codeName(ts_code)
    df["date"]=date
    tmp=df[["tomorrow_high","tomorrow_low","close","date","name","pe_ttm","turnover_rate_f","amp","high","low"]]
    if(tmp.empty==False):
        mydict={c:tmp[c][0] for c in tmp.columns}
        logger.info("{0}-{1}".format(date,mydict))
    else:
        logger.error("Empty Dataframe")
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
    if(today.hour < 19):
        today = today - timedelta(1)
    while(is_cal_date(today.strftime("%Y%m%d"))==False):
        today = today - timedelta(1)
    during=30
    mydates=get_cal_date(end_date=today,during=during)
    print(mydates)
    today=today.strftime("%Y%m%d")
    industry = [  ["银行", "保险"],
         ["化学制药", "生物制药"],
        # ["汽车配件", "汽车整车", "纺织机械"],
        [ "煤炭开采", "石油加工", "石油开采"],
        ["造纸", "水泥"],
        # ["建筑施工", "环境保护", ],
         ["白酒", "乳制品","超市连锁"],
        # ["煤炭开采", "石油加工", "石油开采"],
        # ["特种钢", "矿物制品", "普钢"],
        # ["火力发电", "新型电力", "水利发电"],
        # ["家用电器", "电器仪表", "化工原料"],
        # ["医药商业", "医疗保健", ],
         ["全国地产", "区域地产"],
        #["证券", "保险"]
                  ]
    flatten_list = lambda l: [item for sublist in l for item in sublist]
    if (isinstance(industry[0], list)):
        full_list = get_codelist(flatten_list(industry))
        if (str(full_list[0]).find("S") < 0):
            full_list = list(map(is_SH, full_list))
    # ## 计算所有的指标
    #df = get_daily_feature(today, full_list)
    #df.to_csv("../stock/{0}-fullturnover.csv".format(today), sep="\t", index=False)
    mylist = get_ts_codes()
    df = get_daily_feature(today, mylist)
    if (os.path.exists("../stock") == False):
        os.mkdir("../stock")
    df.to_csv("../stock/{0}-today-turnover.csv".format(today), sep="\t", index=False)
    res=pd.DataFrame()
    for date in mydates:
        #print(date)
        df = get_daily_feature(date, mylist)
        res=res.append(df,ignore_index=True)
    res.sort_values(by=["name","date"],ascending=[True,False]).to_csv("../stock/{0}-{1}-turnover.csv".format(today,during), sep="\t", index=False)


main()