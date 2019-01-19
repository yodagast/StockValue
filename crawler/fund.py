from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,re,copy,codecs

url="http://fund.eastmoney.com/ETFN_jzzzl.html"
url="http://fund.eastmoney.com/cnjy_jzzzl.html"

def get_fund_list(url):
    '''
    给定天天基金基金数据，获取相关信息
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
    res=[]
    for soup in BeautifulSoup(result, 'html.parser').find_all("tr",id=re.compile('^tr')):#.find_all("table", {"class": "dbtable"}):
        #print("id\tname\tgwth\tgwth_rate\tdwjz\tljjz\ty_dwjz\ty_ljjz\tprice\tcut_off")
        #print(soup.get_text(),end="\t")
        #print(cnt,end="\t")
        cnt=cnt+1
        tmp={}
        #print(soup.get("id").replace("tr",""),end="\t")
        tmp["id"]=soup.get("id").replace("tr","")
        #print(soup.find("nobr").get_text().replace("行情基金吧","").strip(),end="\t")
        tmp["name"]=soup.find("nobr").get_text().replace("行情基金吧","").strip()
        ind=1
        for t in soup.find_all("span",{"class":"zhang"}):
            tmp["zhang_{}".format(ind)]=t.get_text()
            ind=ind+1
            #print(tmp.get_text(),end="\t")
        for t in soup.find_all("span",{"class":"ping"}):
            tmp["ping_{}".format(ind)] = t.get_text()
            ind = ind + 1
            #print(tmp.get_text(),end="\t")
        #print(tmp)
        res.append(tmp)
    #print("!!!!!!\n\t\n!!!!!")
    return res

def get_fund_info(code):
    url="http://fund.eastmoney.com/{}.html".format(code)
    url="http://finance.sina.com.cn/fund/quotes/{}/bc.shtml".format(code)
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
        result = urlopen(request).read().decode('utf-8',errors="ignore")
    except urllib.error.URLError as e:
        return soup
    time.sleep(randint(1, 10))
    cnt = 1
    res = []
    for soup in BeautifulSoup(result, 'html.parser').find_all("div",{"class":"fund_data_item"}):
        res.append(soup.get_text())
    return res
        #for tmp in soup.find_all("dl",{"class":"floatleft"}):
        #    print(tmp.get_text())

def get_fund_info1(code):
    url = "http://finance.sina.com.cn/fund/quotes/{}/bc.shtml".format(code)
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
        result = urlopen(request).read().decode("GBK",errors="ignore")
    except urllib.error.URLError as e:
        return soup
    time.sleep(randint(1, 10))
    cnt = 1
    list=[]
    for soup in BeautifulSoup(result, 'html.parser').find_all("div", {"class": "box-hq"}):
        list.append(soup.get_text())
    return list;

def stock_df_to_csv(df,name="cnjj"):
    date = time.strftime("%Y-%m-%d", time.localtime())
    if (os.path.exists("../fund/") == False):
        os.mkdir("../fund/")
    if (os.path.exists("../fund/{}".format(date)) == False):
        os.mkdir("../fund/{}".format(date))
    df.to_csv("../fund/{0}/{1}.csv".format(date,name),sep="\t", index=False)
tmp=get_fund_list(url)
res=pd.DataFrame(tmp)
stock_df_to_csv(res)
res["StructuredFund"]=res["name"].str.contains("A|B|分级",regex=True)
for idx,row in res.iterrows():
    if(row["StructuredFund"]==True):
        continue
    print(row["id"]+"\t"+row["name"]+"\t"+str(row["StructuredFund"]),end="\t")
    res=get_fund_info(row["id"])
    if(len(res)<1):
        res=get_fund_info1(row["id"])
    print(res)

#res.columns=['id', 'name', 'ping_1', 'ping_2', 'ping_3', 'ping_4', 'ping_5','ping_6', 'ping_7', 'ping_8', 'zhang_1', 'zhang_2']