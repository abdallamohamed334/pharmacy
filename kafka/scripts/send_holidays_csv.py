# send_holidays_csv.py
import pandas as pd
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'pharmacy_holidays'
file_path = 'E:/medical project/generate_data/output_data/pharmacy_holidays.csv'

# قراءة البيانات من CSV
df = pd.read_csv(file_path)

# إرسال البيانات واحدة واحدة مع delay
for index, row in df.iterrows():
    producer.send(topic, value=row.to_dict())
    print(f"📤 Sent record {index + 1}/{len(df)}")
    time.sleep(1)  # تأخير ثانية واحدة بين كل رسالة

producer.flush()
print(f"✅ Done. Sent {len(df)} records to topic '{topic}'")
