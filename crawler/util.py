from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_SH(x):
    if(str(x).startswith("6")):
        return x+".SH"
    else:
        return x+".SZ"
def get_codelist(self, industry="银行"):
    '''
        给定行业类型，获取所有该行业的公司股票代码
        :param industry: string or list
        :return:
        '''
    df = ts.get_stock_basics()
    res = []
    if (isinstance(industry, str)):
        tmp = df[["name", "industry", "pe", "pb", ]][(df.industry == industry)]
        return tmp.index.tolist()
        # cond = (df.industry == industry)# & (df.pb > 0.0) & (df.pb < 1.01) & (df.pe > 0.1) & (df.pe < 30.0)
    elif (isinstance(industry, list)):
        for ind in industry:
            tmp = df[["name", "industry", "pe", "pb", ]][(df.industry == ind)]
            tmp_list = tmp.index.tolist()
            res.extend(tmp_list)
    return res
class Version(object):
    @staticmethod
    def get_codelist(self,industry="银行"):
        '''
            给定行业类型，获取所有该行业的公司股票代码
            :param industry: string or list
            :return:
            '''
        df = ts.get_stock_basics()
        res = []
        if (isinstance(industry, str)):
            tmp = df[["name", "industry", "pe", "pb", ]][(df.industry == industry)]
            return tmp.index.tolist()
            # cond = (df.industry == industry)# & (df.pb > 0.0) & (df.pb < 1.01) & (df.pe > 0.1) & (df.pe < 30.0)
        elif (isinstance(industry, list)):
            for ind in industry:
                tmp = df[["name", "industry", "pe", "pb", ]][(df.industry == ind)]
                tmp_list = tmp.index.tolist()
                res.extend(tmp_list)
        return res

