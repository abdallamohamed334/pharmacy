from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, TimestampType

# ⬅️ إنشاء SparkSession مع ClickHouse JDBC jar
spark = SparkSession.builder \
    .appName("KafkaToClickHouse") \
    .getOrCreate()

# ⬅️ تعريف الـ Schema للبيانات القادمة من Kafka
schema = StructType() \
    .add("pharmacy_id", IntegerType()) \
    .add("pharmacy_name", StringType()) \
    .add("city", StringType()) \
    .add("med_name", StringType()) \
    .add("med_code", IntegerType()) \
    .add("available", BooleanType()) \
    .add("stock_qty", IntegerType()) \
    .add("timestamp", TimestampType())

# ⬅️ قراءة البيانات من Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "pharmacy_stock") \
    .option("startingOffsets", "earliest") \
    .load()

# ⬅️ تحويل القيمة من JSON إلى DataFrame باستخدام الـ schema
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# ⬅️ دالة الكتابة إلى ClickHouse باستخدام JDBC
def write_to_clickhouse(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:clickhouse://host.docker.internal:8123/default") \
        .option("dbtable", "pharmacy_stock_new") \
        .option("user", "default") \
        .option("password", "123") \
        .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
        .mode("append") \
        .save()

# ⬅️ تنفيذ الكتابة باستخدام foreachBatch
query = json_df.writeStream \
    .foreachBatch(write_to_clickhouse) \
    .outputMode("append") \
    .start()

query.awaitTermination()
