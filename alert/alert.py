from clickhouse_connect import get_client
import smtplib
from email.mime.text import MIMEText

# الاتصال بـ ClickHouse
client = get_client(
    host='localhost',
    port=8123,
    username='default',
    password='123',
    database='default'
)

# استعلام للكشف عن انخفاض الكمية
query_low_stock = """
SELECT pharmacy_name, med_code, med_name, stock_qty
FROM pharmacy_stock_new
WHERE stock_qty < 10
"""

# استعلام للكشف عن الإجازات الحالية (اليوم أو المستقبل)
query_holidays = """
SELECT p.pharmacy_name, h.date, h.holiday_reason
FROM pharmacy_holidays h
JOIN pharmacy_stock_new p ON h.pharmacy_id = p.pharmacy_id
WHERE h.date >= today()
ORDER BY h.date
"""

# تنفيذ الاستعلامات
result_low_stock = client.query(query_low_stock)
result_holidays = client.query(query_holidays)

# بناء رسالة البريد الإلكتروني
message_body = ""

# تنبيه الأدوية منخفضة الكمية
if result_low_stock.result_rows:
    message_body += "⚠️ تنبيه: يوجد أدوية منخفضة الكمية في الصيدليات:\n\n"
    for row in result_low_stock.result_rows:
        pharmacy_name, med_code, med_name, stock_qty = row
        message_body += f"صيدلية: {pharmacy_name} | {med_name} (كود: {med_code}) | الكمية: {stock_qty}\n"
    message_body += "\n"

# تنبيه الإجازات
if result_holidays.result_rows:
    message_body += "📅 تنبيه: توجد إجازات أو عطلات للصيدليات التالية:\n\n"
    for row in result_holidays.result_rows:
        pharmacy_name, date, holiday_reason = row
        message_body += f"صيدلية: {pharmacy_name} | التاريخ: {date} | السبب: {holiday_reason}\n"
    message_body += "\n"

if message_body:
    # إعداد الإيميل
    msg = MIMEText(message_body)
    msg['Subject'] = '🚨 تنبيه: تحديث حالة الصيدليات'
    msg['From'] = 'pharmacy_report@gmail.com'
    msg['To'] = 'tallaey445@gmail.com'

    # إرسال الإيميل (Gmail كمثال)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('tallaey445@gmail.com', 'pshq ljrr bazn ljew')
        server.send_message(msg)

    print("📩 تم إرسال التنبيه بالبريد الإلكتروني.")
else:
    print("✅ لا يوجد تنبيهات حالياً.")
