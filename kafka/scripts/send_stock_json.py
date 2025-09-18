# send_stock_json.py
import json
import time
from kafka import KafkaProducer

# إعداد البروديوسر
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'pharmacy_stock'
file_path = 'E:/medical project/generate_data/output_data/pharmacy_stock_data.json'

# قراءة الملف JSON (multiline = JSON Array)
with open(file_path, 'r') as f:
    data = json.load(f)  # ده هيرجع list of dicts

# إرسال البيانات واحدة واحدة مع delay
for index, record in enumerate(data):
    producer.send(topic, value=record)
    print(f"📤 Sent record {index + 1}/{len(data)}")
    time.sleep(1)  # تأخير ثانية واحدة بين كل رسالة

producer.flush()
print(f"✅ Done. Sent {len(data)} records to topic '{topic}'")
