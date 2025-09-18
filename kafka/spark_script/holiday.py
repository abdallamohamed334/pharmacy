from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, IntegerType, StringType, DateType

# 1. إنشاء SparkSession
spark = SparkSession.builder \
    .appName("KafkaToClickHouse_Holidays") \
    .getOrCreate()

# 2. تعريف الـ schema
schema = StructType() \
    .add("pharmacy_id", IntegerType()) \
    .add("date", DateType()) \
    .add("holiday_reason", StringType())

# 3. قراءة البيانات من Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "pharmacy_holidays") \
    .option("startingOffsets", "earliest") \
    .load()

# 4. تحويل الـ value من JSON إلى DataFrame
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# 5. دالة الكتابة إلى ClickHouse
def write_to_clickhouse(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:clickhouse://host.docker.internal:8123/default") \
        .option("dbtable", "pharmacy_holidays") \
        .option("user", "default") \
        .option("password", "123") \
        .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
        .mode("append") \
        .save()

# 6. الكتابة باستخدام foreachBatch
query = json_df.writeStream \
    .foreachBatch(write_to_clickhouse) \
    .outputMode("append") \
    .start()

query.awaitTermination()
