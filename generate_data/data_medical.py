import json
import random
from datetime import datetime
from faker import Faker

fake = Faker('ar_EG')  # لتوليد أسماء بالعربي

# قائمة المدن والصيدليات والأدوية
cities = ["Cairo", "Giza", "Alexandria", "Aswan", "Mansoura", "gharbia","portsaid"]
medicines = [
    {"name": "Insulin", "code": 1001},
    {"name": "Paracetamol", "code": 1002},
    {"name": "Augmentin", "code": 1003},
    {"name": "Ventolin", "code": 1004},
    {"name": "Ibuprofen", "code": 1005},
    {"name": "Amoxicillin", "code": 1006},
    {"name": "Metformin", "code": 1007},
    {"name": "Omeprazole", "code": 1008},
    {"name": "Ciprofloxacin", "code": 1009},
    {"name": "Lisinopril", "code": 1010},
    {"name": "Atorvastatin", "code": 1011},
    {"name": "Amlodipine", "code": 1012},
    {"name": "Prednisone", "code": 1013},
    {"name": "Hydrochlorothiazide", "code": 1014},
    {"name": "Simvastatin", "code": 1015},
    {"name": "Levothyroxine", "code": 1016},
    {"name": "Azithromycin", "code": 1017},
    {"name": "Gabapentin", "code": 1018},
    {"name": "Sertraline", "code": 1019},
    {"name": "Zolpidem", "code": 1020}
]


# عدد السجلات اللي هتتولد
num_records = 100

data = []

for _ in range(num_records):
    med = random.choice(medicines)
    available = random.choice([True, False])
    stock = random.randint(0, 50) if available else 0

    record = {
        "pharmacy_id": random.randint(100, 999),
        "pharmacy_name": fake.company(),
        "city": random.choice(cities),
        "med_name": med["name"],
        "med_code": med["code"],
        "available": available,
        "stock_qty": stock,
        "timestamp": datetime.now().isoformat()
    }

    data.append(record)

# حفظ البيانات في ملف JSON
with open("e:/medical project/generate_data/output_data/pharmacy_stock_data.json", "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ تم إنشاء ملف البيانات: pharmacy_stock_data.json")
