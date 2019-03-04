from pyspark.sql import SparkSession

file = "path/README.md"  # Should be some file on your system
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(file).cache()

