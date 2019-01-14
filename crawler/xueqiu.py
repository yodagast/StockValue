from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
def get_html(url,retry_count = 5):
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    delete_proxy(proxy)
    return None

def get_filter_stock_columns(df):
    columns=["code", "name",  "dividend_yield", "eps",  "pe_ttm","current", "high52w",  "low52w","limit_down", "limit_up",
             "current_year_percent","pe_forecast", "pe_lyr","pb" ,"navps", "profit", "profit_four"]
    cond =  (df.pb > 0.0) & (df.eps>0.1)&(df.dividend_yield>0.1)& (df.pe_ttm > 0.1) #& (df.pe_ttm < 30.0)
    df=df[columns][cond]
    return df

def get_stock_info(code):
    '''
    给定股票代码，获取雪球上的相关信息
    :param code:  example:SH601318
    :return: dict
    '''
    if(code[0]=='6'):
        url="https://www.xueqiu.com/S/SH"+str(code)
    else:
        url="https://www.xueqiu.com/S/SZ"+str(code)
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
    for soup in BeautifulSoup(result, 'html.parser').find_all("div", {"class": "stock-compare-box"}):
        left = str(soup).find("<stock-compare :quote=")
        right = str(soup).rfind(",\"quoteMarket")
        soup = str(soup)[left + 23:right] + "}"
    if(len(soup)<5):
        soup = "{}"
    return json.loads(soup)

def get_codelist(industry="银行"):
    '''
    给定行业类型，获取所有该行业的公司股票代码
    :param industry: string or list
    :return:
    '''
    df = ts.get_stock_basics()
    res=[]
    if(isinstance(industry,str)):
        tmp= df[["name", "industry", "pe", "pb",]][(df.industry == industry)]
        return tmp.index.tolist()
        #cond = (df.industry == industry)# & (df.pb > 0.0) & (df.pb < 1.01) & (df.pe > 0.1) & (df.pe < 30.0)
    elif(isinstance(industry,list)):
        for ind in industry:
            tmp = df[["name", "industry", "pe", "pb", ]][(df.industry == ind)]
            tmp_list=tmp.index.tolist()
            res.extend(tmp_list)
    return res

def get_stock_code(industry,SH_only=False):
    codes=get_codelist(industry)
    if(len(codes)<1):
        codes=ts.get_stock_basics().index.tolist()[:10]
    res = pd.DataFrame()
    cnt=1
    for code in codes:
        if((SH_only==True) & (code[0]!='6')):
           continue
        print(str(code)+"\t"+str(cnt))
        cnt=cnt+1
        tmp = pd.DataFrame(get_stock_info(code), index=[0])
        res=res.append(tmp,ignore_index=True)
        #cnt=cnt+1
        #if(cnt>10):
        #    break
    return res

def compute_daily_stock(industry):
    # industry = ["火力发电", "新型电力", "水力发电"]
    # industry = ["小金属", "铝", "铜","普钢","特种钢"]
    # industry =["水务","环境保护","园区开发"]
    # industry=["房产服务","家用电器","水泥","全国地产"]
    # industry = ["煤炭开采", "石油贸易", "石油加工"]
    # industry=["医药商业", "医疗保健",]
    # industry = [ "化学制药", "生物制药", "中成药"]
    res = get_stock_code(industry)
    date = time.strftime("%Y-%m-%d", time.localtime())
    if (isinstance(industry, list)):
        industry = "-".join(industry)
        print(industry, end="\t")
    if (os.path.exists("../data/{}".format(date)) == False):
        os.mkdir("../data/{}".format(date))
    get_filter_stock_columns(res).sort_values(by=["eps", "current_year_percent", "pe_ttm"], ascending=[False, False, True]) \
        .to_csv("../data/{0}/{1}.csv".format(date, industry), sep="\t", index=False)
    print(res.shape)
    time.sleep(300)
    time.sleep(randint(1, 20))


def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    #industry=[["化学制药","生物制药","中成药"],["铝", "普钢","特种钢"],
    #          ["证券", "保险",],[ "银行","造纸"],
    #          ["家用电器","汽车整车","汽车服务"],["煤炭开采", "石油贸易", "石油加工"]]
    industry = [["化学制药", "生物制药", "中成药"],["证券", "保险",],
                [ "银行","造纸"],["煤炭开采", "石油贸易", "石油加工","交通运输"],
                ["家用电器","汽车整车","汽车服务","电器连锁"],["火力发电","新型电力","水利发电"],
                ["医药商业","医疗保健","超市连锁"],["白酒","乳制品"]]
    if(len(industry)<1):
        return ;
    elif(isinstance(industry[0],list)):
        for ind in industry:
            compute_daily_stock(ind)
    else:
        compute_daily_stock(industry)
    #industry = ["医药商业","医疗保健","化学制药","生物制药","中成药"]
    #industry = ["证券", "保险", "银行"]



if __name__ == "__main__":
    scheduler=BlockingScheduler()
    scheduler.add_job(main,'cron', day_of_week='1-5', hour=9, minute=17)
    scheduler.start()
    #sys.exit(main())

#print(res.head(2))
#res_json=get_stock_info("002027")
#print(res_json)
#tmp=pd.DataFrame(res_json,index=[0])
#print(tmp.head(2))


