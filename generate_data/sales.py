import csv
import random
from datetime import datetime, timedelta

# قائمة الصيدليات (نفس اللي استخدمناها قبل كده)
pharmacy_ids = [101, 102, 103, 104, 105]

# قائمة الأدوية مع الكود
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
]

# عدد الأيام اللي هنولد بيانات ليها (آخر 30 يوم)
num_days = 30

# اسم ملف CSV
file_name = "e:/medical project/generate_data/output_data/medicine_sales_data.csv"

# توليد البيانات
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # كتابة الهيدر
    writer.writerow(["pharmacy_id", "med_code", "date", "units_sold"])

    for day_offset in range(num_days):
        current_date = (datetime.now() - timedelta(days=day_offset)).date()
        for pharmacy_id in pharmacy_ids:
            for med in medicines:
                # توليد عدد مبيعات عشوائي (بعض الأيام ممكن ما يكونش فيه مبيعات)
                units_sold = random.choices([0, random.randint(1, 50)], weights=[0.3, 0.7])[0]
                writer.writerow([pharmacy_id, med["code"], current_date.isoformat(), units_sold])

print(f"✅ تم إنشاء ملف مبيعات الأدوية: {file_name}")
