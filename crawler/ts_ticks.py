from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date

from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import tushare as ts
import h5py as f
import sys,getopt,time,json,requests,urllib,os,platform,logging
from util import get_codelist
from util import *

logging.basicConfig(level=logging.INFO, format=' %(message)s ')
logger = logging.getLogger(__name__)

df = ts.get_tick_data('600848',date='2018-12-12',src='tt')

def main():
    #today = get_recent_date()
    end_date = get_recent_date()
    lastyear_dates=get_cal_date(isPro=False)
    mycodes=get_ts_codes(isPro=False)
    logger.info("processing dates in {}".format(lastyear_dates))
    logger.info("processing codes in {}".format(mycodes))
    if (os.path.exists("../ticks") == False):
        os.mkdir("../ticks")
        #store = HDFStore("../ticks/ticks")
        #h5file = f.File("../ticks/ticks", 'w')
    cnt=0
    for code in mycodes:
        res=pd.DataFrame()
        for date in lastyear_dates:
            logger.info("processing {0} on date {1}".format(code,date))
            df = ts.get_tick_data(code, date=date, src='sn')
            print(df.head(2))
            res=res.append(df,ignore_index=True)
            time.sleep(0.3)
            df.to_hdf('../ticks/ticks.h5', '{0}_{1}'.format(code,date))
        cnt=cnt+1
        if(cnt>5):
            return
        res.to_csv("../ticks/{0}-ticks.csv".format(code), sep="\t", index=False)

main()