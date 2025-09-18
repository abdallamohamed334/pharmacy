# stream_holidays_to_hdfs.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, DateType

spark = SparkSession.builder.appName("KafkaToHDFS_Holidays").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("pharmacy_id", IntegerType()) \
    .add("holiday_date", DateType()) \
    .add("holiday_name", StringType())

df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "pharmacy_holidays") \
    .option("startingOffsets", "latest") \
    .load()

df_value = df_kafka.selectExpr("CAST(value AS STRING) as json_str")

df_parsed = df_value.select(from_json(col("json_str"), schema).alias("data")).select("data.*")

query = df_parsed.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/data/raw/stream/holidays/") \
    .option("checkpointLocation", "/tmp/checkpoints/holidays/") \
    .outputMode("append") \
    .start()

query.awaitTermination()
