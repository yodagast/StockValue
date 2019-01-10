from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os

def get_stock_AH(url="https://xueqiu.com/hq#AH"):
    '''
    获取A-H价格对比
    :param code:  example:SH601318
    :return: dict
    '''
    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36''',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate', 'accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cache-control': 'max-age=0', 'connection': 'keep-alive',
        'referer': 'www.bing.com'
    }
    headers = {'User-Agent': 'Mozilla/5.0'}
    soup = {}
    request = Request(url, headers=headers)  # ('https://xueqiu.com/S/SH601318')
    try:
        result = urlopen(request).read().decode('utf-8')
    except urllib.error.URLError as e:
        return soup
    #result=urlopen(request).read().decode('utf-8')
    #result=get_html(url)
    time.sleep(randint(1,10))
    for soup in BeautifulSoup(result, 'html.parser').find_all("div",{"class":"stocklist-wrapper"}):
        print(soup)
        left = str(soup).find("<stock-compare :quote=")
        right = str(soup).rfind(",\"quoteMarket")
        soup = str(soup)[left + 23:right] + "}"
    if(len(soup)<5):
        soup = "{}"
    return json.loads(soup)

def main():
    url="http://www.szse.cn/certificate/individual/index.html?code=000001"
