from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import sys,getopt,time,json,requests,urllib

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

def get_stock_columns(df):
    columns=["code", "name", "current", "high", "high52w", "low", "low52w","limit_down", "limit_up",
             "current_year_percent", "dividend_yield", "eps","navps", "pb", "pe_forecast", "pe_lyr", "pe_ttm", "profit", "profit_four"]
    return df[columns]

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

def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    industry = ["小金属","铝","铜","普钢"]
    res = get_stock_code(industry)
    date = time.strftime("%Y-%m-%d", time.localtime())
    if (isinstance(industry, list)):
        industry = "-".join(industry)
    get_stock_columns(res).sort_values(by=["current_year_percent", "eps", "pe_ttm"], ascending=[False, False, True]) \
        .to_csv("../data/{0}-{1}.csv".format(industry, date), sep="\t", index=False)
    print(res.shape)
if __name__ == "__main__":
    sys.exit(main())

#print(res.head(2))
#res_json=get_stock_info("002027")
#print(res_json)
#tmp=pd.DataFrame(res_json,index=[0])
#print(tmp.head(2))


