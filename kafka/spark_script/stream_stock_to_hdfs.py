# stream_stock_to_hdfs.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, BooleanType, TimestampType

spark = SparkSession.builder.appName("KafkaToHDFS_Stock").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# تعريف السكيمـا
schema = StructType() \
    .add("pharmacy_id", IntegerType()) \
    .add("pharmacy_name", StringType()) \
    .add("city", StringType()) \
    .add("med_name", StringType()) \
    .add("med_code", IntegerType()) \
    .add("available", BooleanType()) \
    .add("stock_qty", IntegerType()) \
    .add("timestamp", TimestampType())

# قراءة من Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "pharmacy_stock") \
    .option("startingOffsets", "latest") \
    .load()

df_value = df_kafka.selectExpr("CAST(value AS STRING) as json_str")

df_parsed = df_value.select(from_json(col("json_str"), schema).alias("data")).select("data.*")

# الكتابة إلى HDFS كـ Parquet
query = df_parsed.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/data/raw/stream/stock/") \
    .option("checkpointLocation", "/tmp/checkpoints/stock/") \
    .outputMode("append") \
    .start()

query.awaitTermination()
