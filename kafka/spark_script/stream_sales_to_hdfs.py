# stream_sales_to_hdfs.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType, TimestampType

spark = SparkSession.builder.appName("KafkaToHDFS_Sales").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("sale_id", IntegerType()) \
    .add("pharmacy_id", IntegerType()) \
    .add("med_code", IntegerType()) \
    .add("quantity", IntegerType()) \
    .add("sale_amount", FloatType()) \
    .add("timestamp", TimestampType())

df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "pharmacy_sales") \
    .option("startingOffsets", "latest") \
    .load()

df_value = df_kafka.selectExpr("CAST(value AS STRING) as json_str")

df_parsed = df_value.select(from_json(col("json_str"), schema).alias("data")).select("data.*")

query = df_parsed.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/data/raw/stream/sales/") \
    .option("checkpointLocation", "/tmp/checkpoints/sales/") \
    .outputMode("append") \
    .start()

query.awaitTermination()
