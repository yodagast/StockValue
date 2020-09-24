from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
import talib as ta
from urllib.parse import urlencode
from crawler.util import *
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro=ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
pd.set_option('display.max_colwidth',500)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr',False)

url="http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?"
headers={'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}

def get_freq_df(params={"symbol":"sz000002","scale":30,"ma":"no","datalen":240}):
    '''
    :param params: 获取股票分钟级别数据
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

def MA(df,timeperiod=5):
    df['ma_5'] = pd.rolling_mean(df['close'], timeperiod)
    return df

def KDJ(df):
    '''
    K线是快速确认线——数值在90以上为超买,数值在10以下为超卖;
    D是慢速主干线——数值在80以上为超买,数值在20以下为超卖;
    J为方向敏感线, 当J值大于100,特别是连续5天以上,至少会形成短期头部,反之J值小于0时,股价至少会形成短期底部。
    :param df:
    :return:
    '''
    low_list = df['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    high_list = df['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    df['K'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    df['KDJ'] = ''
    kdj_position = df['K'] > df['D']
    df.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ'] = 'gold'
    df.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ'] = 'dead'
    df=df[df["KDJ"]!=""]
    return df

def WR(df):
    '''
    适合短线交易：WR=（H—C）÷（H—L）
    1．当威廉指数线高于85，市场处于超卖状态，行情即将见底。
    2．当威廉指数线低于15，市场处于超买状态，行情即将见顶。
    3．与相对强弱指数配合使用，可得出对大市走向较为准确的判断。
    :param df:
    :return:
    '''
    df['wr'] = ta.WILLR(df['high'].values,
                        df['low'].values,
                        df['close'].values,
                        timeperiod=14)
    return df

def BOLL(df):
    '''
    upper： 中轨线=N日的移动平均线
    middle： 上轨线=中轨线+K倍的标准差
    lower： 下轨线=中轨线－K倍的标准差（K为参数，可根据股票的特性来做相应的调整，一般默认为2）
    (1) 股价高于这个波动区间，即突破阻力线，说明股价虚高，故卖出
    (2) 股价低于这个波动区间，即跌破支撑线，说明股价虚低，故买入
    :param df:
    :return:
    '''
    df.index = range(len(df))
    df['boll_upper'], df['boll_middle'], df['boll_lower'] = ta.BBANDS(
        df.close.values,
        timeperiod=20,
        # number of non-biased standard deviations from the mean
        nbdevup=2,
        nbdevdn=2,
        # Moving average type: simple moving average here
        matype=0)
    return df

def RSI(df):
    '''
    RSI＝[上升平均数/(上升平均数＋下跌平均数)]×100
    上升平均数：在某一段日子里升幅数的平均；下跌平均数：在同一段日子里跌幅数的平均。
    当RSI高于70时，股票可以被视为超买，是卖出的时候。
    当RSI低于30时，股票可以被视为超卖，是买入的时候。
    :param df:
    :return:
    '''
    df["rsi"] = ta.RSI(df["close"].values, timeperiod=14)
    return df

def OBV(df):
    df["obv"] = ta.OBV(df['close'].values, df['vol'].values)
    return df

def MACD(df):
    df['ema_12'] = ta.EMA(df["close"].values, timeperiod=6)
    df['ema_26'] = ta.EMA(df["close"].values, timeperiod=12)
    df['macd'], df['macd_singal'], df['macd_hist'] = ta.MACD(df["close"].values,
                                                              fastperiod=6, slowperiod=12, signalperiod=9)
    return df
def MOM(df,timeperiod=5):
    df['mom'] = ta.MOM(df["close"].values, timeperiod)
    return df
def OBV(df,k=0.1):
    '''
    当股价上升而OBV线下降，表示买盘无力，股价可能会回跌。
    股价下降时而OBV线上升，表示买盘旺盛，逢低接手强股，股价可能会止跌回升。
    :param df:
    :param k:
    :return:
    '''
    df['obv']=df['vol']*(2*df["close"]-df['high']-df['low']+k)/(df['high']-df['low']+k)
    return df
def BIAS(df):
    return
#df = pro.daily(ts_code='601601.SH', start_date='20200201', end_date='20200411')
df=get_freq_df()
print(KDJ(df))