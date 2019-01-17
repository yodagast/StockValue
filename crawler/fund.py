from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,re

url="http://fund.eastmoney.com/ETFN_jzzzl.html"

def get_stock_info(url):
    '''
    给定股票代码，获取雪球上的相关信息
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
        result = urlopen(request).read().decode('GBK')
    except urllib.error.URLError as e:
        return soup
    #result=urlopen(request).read().decode('utf-8')
    #result=get_html(url)
    time.sleep(randint(1,10))
    cnt=1
    print("索引\t基金代码\t基金名\t增长值\t增长率\t单位净值\t累计净值\t单位净值(昨)\t累计净值(昨)\t市价\t折价率")
    for soup in BeautifulSoup(result, 'html.parser').find_all("tr",id=re.compile('^tr')):#.find_all("table", {"class": "dbtable"}):
        #print("id\tname\tgwth\tgwth_rate\tdwjz\tljjz\ty_dwjz\ty_ljjz\tprice\tcut_off")
        #print(soup.get_text(),end="\t")
        print(cnt,end="\t")
        cnt=cnt+1
        print(soup.get("id").replace("tr",""),end="\t")
        print(soup.find("nobr").get_text().replace("行情基金吧","").strip(),end="\t")
        for tmp in soup.find_all("span",{"class":"zhang"}):
            print(tmp.get_text(),end="\t")
        for tmp in soup.find_all("span",{"class":"ping"}):
            print(tmp.get_text(),end="\t")
        print()
    #return json.loads(soup)

get_stock_info(url)