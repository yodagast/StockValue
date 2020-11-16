from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import *
from py4j.java_collections import MapConverter
import shutil,configparser,logging,os
import threading
from pyspark.sql import SparkSession
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
def filter_parquet(string):
    return string.find("parquet") > 0

def parquet2delta(input_dir="./202006/",output_path="./delta/"):
    df = spark.read.parquet(input_dir)
    df.write.format("delta").partitionBy("Date").mode("append").save(output_path)
    logger.info("write df %s sucessful" % input_dir)

def parquet2delta_fn(pp='price'):
    config = configparser.ConfigParser()
    config.read("../data/config.cfg")
    input_dir = config.get("Delta", "home_dir")
    ohlcv_dir = config.get("Delta", "ohlcv_dir")
    price_dir = config.get("Delta", "price_dir")
    logger.info(input_dir + "|||\t " + ohlcv_dir +"|||\t "+price_dir)
    output_dir=price_dir
    if(pp=='ohlcv'):
        output_dir=ohlcv_dir
    for par_dir in filter(filter_parquet,os.listdir(input_dir)):
        pp = os.path.join(input_dir, par_dir,"price.parquet")
        logger.info(pp)
        parquet2delta(pp, output_dir)

spark = SparkSession.builder.appName("MyApp") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:0.7.0") \
        .config("spark.driver.extraJavaOptions","-XX:+UseG1GC") \
        .config("spark.sql.autoBroadcastJoinThreshold","-1") \
        .config("spark.python.worker.memory","5g") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
#parquet2delta_fn()
def get_price():
    pp = "/media/yodagast/RADAGAST/stock/price_delta"
    codes=str('600036.SH,601601.SH,300498.SZ,000002.SZ,601318.SH,601166.SH').split(",")
    config = configparser.ConfigParser()
    config.read("../data/config.cfg")
    codes = config.get("Stock", "codes").split(",")
    df = spark.read.format('delta').load(pp). \
        filter(F.col("Date").between('2020-07-01', '2020-08-10'))
    tmp=df.filter(df.Code.isin(codes))
    print(tmp.columns)
    tmp.groupby(["Code","Date"]).agg(F.max("Price"),F.min("Price"),F.max("Vol")).sort(["Code","Date"]).show(10000)
get_price()