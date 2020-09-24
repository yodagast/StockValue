from pyspark.sql import SparkSession
import pyspark
import delta
import pyarrow as pa
import pyarrow.parquet as pq
from crawler.util import *
from pyunpack import Archive
import configparser,shutil

from pyspark.sql import Column, DataFrame, SparkSession, functions
from pyspark.sql.functions import *
from py4j.java_collections import MapConverter
import shutil
import threading

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
pro = ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')


def str2date(str):
    return datetime.strptime(str, "%Y%m%d")

def date2str(date, date_formate="%Y-%m-%d"):
    return date.strftime(date_formate)

def jd_data_writer(path="./2020-09/",start='20200901',end='20200919'):
    df = pro.trade_cal(exchange='SSE', start_date=start, end_date=end)
    df=df[df["is_open"]==1]
    for idx,dat in df.iterrows():
        date=date2str(str2date(dat['cal_date']))
        url="http://ohlc1s.s3.cn-east-2.jdcloud-oss.com/{}.7z".format(date)
        if (os.path.exists(path + date + ".7z") and os.path.getsize(path + date + ".7z") / float(1024 * 1024) >50):
            logger.info("{%s} exists" % date)
            continue
        cmd="curl -o {} {}".format(path+date+".7z",url)
        logger.info(cmd)
        os.system(cmd)
    return

def check_file(path="./2020-09/",start='20200901',end='20200914'):
    df = pro.trade_cal(exchange='SSE', start_date=start, end_date=end)
    df = df[df["is_open"] == 1]
    for idx, dat in df.iterrows():
        date = date2str(str2date(dat['cal_date']))
        if (os.path.getsize(path+date+".7z")/float(1024*1024)<50):
            jd_data_writer(path,start=dat["cal_date"],end=dat["cal_date"])
        else:
            print("date %s checked" %dat["cal_date"] )
        if(os.path.getsize(path+date+".7z")/float(1024*1024)<50):
            print("get error %s" % dat["cal_date"])
    return





def ts_daily_data(path='./',start_date='20180101',end_date='20191231'):
    df = pro.trade_cal(exchange='SSE', start_date=start_date, end_date=end_date)
    df = df[df["is_open"] == 1]
    for idx, dat in df.iterrows():
        tmp = pro.query('daily_basic', ts_code='',trade_date=dat['cal_date'])
        table = pa.Table.from_pandas(tmp)
        if (table != None):
            pq.write_to_dataset(table, root_path=path + "{}_{}.parquet".format(start_date, end_date))
            logger.info("save {} success".format(dat['cal_date']))
            time.sleep(10)
    logger.info(df.columns)

def z7file_transformer(input_dir="./",output_dir="./202006/"):
    for path,dir_list,file_list in os.walk(input_dir):
        logger.info(path)
        def filter7z(string):
            return string.find("7z")>1
        logger.info(list(filter(filter7z,file_list)))
        for file in filter(filter7z,file_list):
            logger.info("extracting file {}".format(file))
            Archive(os.path.join(input_dir,file)).extractall(output_dir)

def archive_7z(path,start='20200701',end='20200710'):
    df = pro.trade_cal(exchange='SSE', start_date=start, end_date=end)
    df = df[df["is_open"] == 1]
    for idx, dat in df.iterrows():
        date = date2str(str2date(dat['cal_date']))
        logger.info(os.path.join(path, date+".7z"))
        Archive(os.path.join(path, date+".7z")).extractall(path)



def filter_price(string):
    return string.find("PRICE") > 0
def filter_ohlcv(string):
    return string.find("OHLCV") > 0
def filter_parquet(string):
    return string.find("parquet") > 0
def csvfile_extract(input_dir="./2020-06/",file_name="2020-06-29.7z"):
    logger.info("extracting file {}".format(file_name))
    Archive(os.path.join(input_dir, file_name)).extractall(input_dir)

def parquet2delta(input_dir="./202006/",output_path="./delta/"):
    spark = SparkSession.builder \
        .appName("quickstart") \
        .master("local[*]") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    df = spark.read.parquet(input_dir)
    df.write.format("delta").partitionBy("Date").save(output_path)
    logger.info("write df sucessful")

def parquet2delta_fn():
    config = configparser.ConfigParser()
    config.read("./config.cfg")
    input_dir = config.get("Paths", "home_dir")
    delta_dir = config.get("Paths", "parquet_dir")
    logger.info(input_dir + "\t" + delta_dir)
    for par_dir in filter(filter_parquet,os.listdir(input_dir)):
        pp = os.path.join(input_dir, par_dir,"price.parquet")
        logger.info(pp)
        parquet2delta(pp, delta_dir)

#parquet2delta_fn()

def csv2parquet(input_dir="./202006/",output_path="./2006/"):
    for path, dir_list, file_list in os.walk(input_dir):
        logger.info(file_list)
        price = filter(filter_price, file_list)
        ohlcv= filter(filter_ohlcv,file_list)
        for file in price:
            logger.info(os.path.join(input_dir,file))
            df=pd.read_csv(os.path.join(input_dir,file),header=0)
            logger.info(df.head(2))
            table = pa.Table.from_pandas(df)
            pq.write_to_dataset(table, root_path=os.path.join(output_path,"price.parquet"),partition_cols=["Date"],compression='gzip')
        for file in ohlcv:
            logger.info(os.path.join(input_dir,file))
            df=pd.read_csv(os.path.join(input_dir,file),header=0)
            df['Date'] = df["Time"].apply(lambda x: x[:10])
            logger.info(df.head(2))
            table = pa.Table.from_pandas(df)
            pq.write_to_dataset(table, root_path=os.path.join(output_path,"ohlcv.parquet"),partition_cols=["Date"],compression='gzip')

def rm_csves(csv_dir):
    def filter_csv(string):
        return string.find("csv")>0
    for path,dir_list,file_list in os.walk(csv_dir):
        logger.info(file_list)
        for file in filter(filter_csv,file_list):
            os.remove(os.path.join(path,file))
            logger.info("{} is removed".format(os.path.join(path,file)))


def main(removeable=True):
    config = configparser.ConfigParser()
    config.read("./config.cfg")
    input_dir=config.get("Paths","Z7_dir")
    parquet_dir=config.get("Paths","parquet_dir")
    logger.info(input_dir+"\t"+parquet_dir)
    if(removeable==True and os.path.exists(parquet_dir)):
        shutil.rmtree(parquet_dir)
    elif(removeable==False and os.path.exists(parquet_dir)):
        print("{} not removed".format(parquet_dir))
    else:
        os.mkdir(parquet_dir)
    #archive_7z(input_dir)
    rm_csves(input_dir)
    z7file_transformer(input_dir,input_dir)
    csv2parquet(input_dir,parquet_dir)
    rm_csves(input_dir)


#jd_data_writer()
#check_file()
main()
