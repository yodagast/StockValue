from urllib.request import Request, urlopen
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta,date
from pyspark.sql import SparkSession
from pyspark.sql import column
from random import randint
import pandas as pd
from pprint import pprint
import tushare as ts
import sys,getopt,time,json,requests,urllib,os,platform,logging
import configparser,shutil
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def price_data_30day(path,codes):
    df=pd.read_parquet(os.path.join(path,"price.parquet"))
    logger.info(df.head())
    df=df[df["Code"].isin(codes)]
    logger.info(df.head(2))
    return df

def ohlcv_data_30day(path,codes):
    spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
    df=spark.read.parquet(os.path.join(path,"ohlcv.parquet/Date=2020-06-1*"))
    logger.info(df.head(3))
    df=df.filter(df["Code"].isin(codes))
    logger.info(df.head(3))
    return df

def main():
    config = configparser.ConfigParser()
    config.read("./config.cfg")
    codes_dir=config.get("Stocks","codes_dir")
    logger.info("read parquet data from %s" % codes_dir)
    codes=config.get("Stocks","codes").split(",")
    logger.info("stocks codes : %s" % codes)
    price_data_30day(codes_dir,codes)

main()