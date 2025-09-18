from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("UploadFilesToHDFS").getOrCreate()


local_stock_path = "/opt/bitnami/spark/jobs/data/pharmacy_stock_data.json"
local_sales_path = "/opt/bitnami/spark/jobs/data/medicine_sales_data.csv"
local_holidays_path = "/opt/bitnami/spark/jobs/data/pharmacy_holidays.csv"


hdfs_stock_path = "hdfs://namenode:8020/data/raw/pharmacy_stock/"
hdfs_sales_path = "hdfs://namenode:8020/data/raw/pharmacy_sales/"
hdfs_holidays_path = "hdfs://namenode:8020/data/raw/pharmacy_holidays/"


df_stock = spark.read.option("multiline", "true").json(local_stock_path)
df_stock.write.mode("overwrite").parquet(hdfs_stock_path)


df_sales = spark.read.option("header", True).csv(local_sales_path)
df_sales.write.mode("overwrite").parquet(hdfs_sales_path)

df_holidays = spark.read.option("header", True).csv(local_holidays_path)
df_holidays.write.mode("overwrite").parquet(hdfs_holidays_path)


spark.stop()
