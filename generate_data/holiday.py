import csv
import random
from datetime import datetime, timedelta

# صيدليات عشوائية
pharmacy_ids = [101, 102, 103, 104, 105]

# أسباب العطلات الممكنة
holiday_reasons = [
    "إجازة رسمية",
    "صيانة داخلية",
    "ظرف طارئ",
    "وفاة أحد العاملين",
    "عطلة أسبوعية",
    "مشكلة كهرباء"
]

# عدد العطلات اللي هنولدها (عشوائي لكل صيدلية)
holidays_data = []
for pharmacy_id in pharmacy_ids:
    # نحدد عدد العطلات (من 0 إلى 2 لكل صيدلية)
    num_holidays = random.randint(0, 2)
    dates = random.sample(range(1, 30), num_holidays)  # أيام عشوائية في سبتمبر

    for day in dates:
        date = datetime(2025, 9, day).date().isoformat()
        reason = random.choice(holiday_reasons)
        holidays_data.append([pharmacy_id, date, reason])

# كتابة البيانات في ملف CSV
file_name = "e:/medical project/generate_data/output_data/pharmacy_holidays.csv"
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["pharmacy_id", "date", "holiday_reason"])
    writer.writerows(holidays_data)

print(f"✅ تم إنشاء ملف عطلات الصيدليات: {file_name}")
