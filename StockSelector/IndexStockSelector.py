### 指数增强策略
from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
pd.set_option('display.max_colwidth',500)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr',False)

def indexSelector():
    df = pro.index_basic(market='SW')
    ts_code=df["ts_code"].tolist()
    names = df["name"].tolist()
    for code,name in zip(ts_code,names):
        index_df=pro.index_member(index_code=code)
        print(code,name,index_df.head(3))
        if(len(index_df)<1):
            time.sleep(1)
            continue
        else:
            print(os.getcwd())
            index_df.to_csv("./sw/{0}-{1}.csv".format(str(code).replace(".","-"),name), sep="\t", index=False)
            time.sleep(2)

def csv2json(path="./sw/"):
    d={}
    for file in os.listdir(path):
        df=pd.read_csv(path+file,sep="\t",)
        key=file.replace(".csv","")
        val=list(df["con_code"].values)
        d[key]=val
    import json
    json.dump(d,open("index.json","w"))
    return
#csv2json()
import json
d=json.load(open("index.json","r"))
for k in d.keys():
    print(k,d[k])
    break




