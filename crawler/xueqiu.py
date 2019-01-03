from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import time,json,requests,urllib

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
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None

def get_stock_info(code):
    '''
    :param code:  example:SH601318
    :return: dict
    '''
    if(code[0]=='6'):
        url="https://www.xueqiu.com/S/SH"+str(code)
    else:
        url="https://www.xueqiu.com/S/SZ"+str(code)
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)  # ('https://xueqiu.com/S/SH601318')
    try:
        result = urlopen(request).read().decode('utf-8')
    except urllib.error.URLError as e:
        return {}
    #result=urlopen(request).read().decode('utf-8')
    #result=get_html(url)
    time.sleep(randint(3,27))
    for soup in BeautifulSoup(result, 'html.parser').find_all("div", {"class": "stock-compare-box"}):
        left = str(soup).find("<stock-compare :quote=")
        right = str(soup).rfind(",\"quoteMarket")
        soup = str(soup)[left + 23:right] + "}"
    return json.loads(soup)


def get_stock_code():
    codes=ts.get_stock_basics().index.tolist()
    res = pd.DataFrame()
    #cnt=0
    for code in codes:
        print(code)
        tmp = pd.DataFrame(get_stock_info(code), index=[0])
        res=res.append(tmp,ignore_index=True)
        #cnt=cnt+1
        #if(cnt>10):
        #    break
    return res

res=get_stock_code()
date=time.strftime("%Y-%m-%d",time.localtime())
res.to_csv("../data/{}.csv".format(date),sep="\t",index=False)
print(res.shape)
#print(res.head(2))
#res_json=get_stock_info("002027")
#print(res_json)
#tmp=pd.DataFrame(res_json,index=[0])
#print(tmp.head(2))


