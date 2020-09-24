from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
from urllib.parse import urlencode
from crawler.util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

url="http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?"
headers={'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}
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

def get_freq_df(params={"symbol":"sz000002","scale":5,"ma":"no","datalen":240}):
    '''
    :param params: 获取5/30/60/day 数据
    :return:
    '''
    cols = ["day", "open", "high", "low", "close", "volume"]
    s=url+urlencode(params)
    print(s)
    response = requests.get(s)
    str_dict=response.text
    for key in cols:
        str_dict=str_dict.replace(key,"\"{}\"".format(key))
    df=pd.read_json(str_dict, orient='records')
    print(df.head())
    return df
def get_vol_df(params={"symbol":"sz000002","num":9000}):
    '''
    :param params: 获取分笔数据
    :return:
    '''
    url='http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?'
    s = url + urlencode(params)
    print(s)
    response = requests.get(s)
    text_dict = response.text
    text_dict=text_dict.replace("var trade_item_list = new Array();","")
    text_list=text_dict.split(");")
    res=[]
    for i in range(len(text_list)-1):
        data=list(text_list[i].split("new Array(")[1].split(", "))
        print(data)
        res.append(data)
    res = pd.DataFrame(res)
    res=res.applymap(lambda x:str(x).replace("\'",""))
    res.columns=["time","vol","prices","up_down"]
    print(res.head())

def main():
    get_vol_df()

main()