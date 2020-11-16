from pyspark.sql import SparkSession
from operator import add

dict = {'苹果':0,'华为':0,'小米':0,'OPPO':0,'VIVO':0}
spark = SparkSession.builder.appName("wordCount").getOrCreate()
data = spark.read.format("org.apache.spark.sql.execution.datasources.csv.CSVFileFormat").option("header","true").option("inferSchema","false").option("delimiter",",").load('/tmp/wordlist.csv')
# 给2分 只判断string in dict.keys()酌情给1分
def filterString(string):
    for key in dict.keys():
        if (str(string).find(key)>0):
            return True
    return False
# 给1分
def upperString(string):
    return str(string).upper()

#给3分 类似词频统计，增加字符串大写和过滤 关键flatMap reduceByKey等函数
result = data.flatMap(lambda x: x.split(" "))\
        .map(lambda x:upperString(x))\
        .filter(lambda x:filterString(x))\
        .map(lambda x: (x, 1))\
        .reduceByKey(add)

##其他部分酌情给分
for k, v in result:
	if dict.get(k):
		print (k, v)