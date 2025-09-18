import streamlit as st
import pandas as pd
import clickhouse_connect

# الاتصال بـ ClickHouse
client = clickhouse_connect.get_client(
    host='host.docker.internal',  # أو localhost حسب حالتك
    port=8123,
    username='default',
    password='123'
)

st.set_page_config(page_title="Pharmacy Overview", layout="wide")
st.title("📊 Pharmacy Summary Dashboard")

# ---- الاستعلامات ----

# ✅ عدد الصيدليات
pharmacy_count = client.query("SELECT COUNT(DISTINCT pharmacy_id) AS total_pharmacies FROM pharmacy_stock_new").result_rows[0][0]

# ✅ إجمالي الكميات المتاحة في المخزون
total_stock_qty = client.query("SELECT SUM(stock_qty) AS total_stock FROM pharmacy_stock_new").result_rows[0][0]

# ✅ إجمالي مبيعات كل علاج (من جدول المبيعات)
sales_query = """
    SELECT 
        med_code, 
        SUM(units_sold) AS total_units_sold 
    FROM pharmacy_sales 
    GROUP BY med_code 
    ORDER BY total_units_sold DESC
    LIMIT 20
"""
sales_result = client.query(sales_query)
sales_df = pd.DataFrame(sales_result.result_rows, columns=sales_result.column_names)

city_query = """
    SELECT 
        city, 
        SUM(stock_qty) AS total_units_sold 
    FROM pharmacy_stock_new 
    GROUP BY city 
    ORDER BY total_units_sold DESC 
    LIMIT 10
"""

city_result = client.query(city_query)
city_df = pd.DataFrame(city_result.result_rows, columns=city_result.column_names)

st.subheader("🔝 أكثر المحافظات بيعًا")
st.bar_chart(city_df.set_index("city"))

# ---- العرض في Streamlit ----
query = """
SELECT
    ps.pharmacy_id,
    ps.med_code,
    ps.units_sold,
    pn.available,
    pn.stock_qty,
    toDate(ps.date) AS sale_date
FROM pharmacy_sales ps
LEFT JOIN pharmacy_stock_new pn
    ON ps.med_code = pn.med_code
    AND toDate(ps.date) = toDate(pn.timestamp)
ORDER BY sale_date
"""

result = client.query(query)
df = pd.DataFrame(result.result_rows, columns=result.column_names)
df['sale_date'] = pd.to_datetime(df['sale_date'])

min_date = df['sale_date'].min().to_pydatetime()
max_date = df['sale_date'].max().to_pydatetime()

selected_date_range = st.slider(
    "اختر فترة التاريخ",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

filtered_df = df[(df['sale_date'] >= selected_date_range[0]) & (df['sale_date'] <= selected_date_range[1])]

st.dataframe(filtered_df)

col1, col2 = st.columns(2)

with col1:
    st.metric("🏥 عدد الصيدليات", pharmacy_count)

with col2:
    st.metric("📦 إجمالي الكميات في المخزون", total_stock_qty)

st.markdown("## 💊 أكثر الأدوية مبيعًا")
st.dataframe(sales_df, use_container_width=True)


target_cities = ("Cairo", "Giza", "Alexandria", "Aswan", "Mansoura", "gharbia", "portsaid")

# بناء استعلام SQL باستخدام IN
query = f"""
SELECT pharmacy_id, pharmacy_name, city, med_name, med_code, available, stock_qty, timestamp
FROM pharmacy_stock_new
WHERE city IN {target_cities}
"""

# تنفيذ الاستعلام
result = client.query(query)
df = pd.DataFrame(result.result_rows, columns=result.column_names)

# تأكد أن التواريخ بصيغة صحيحة
df['timestamp'] = pd.to_datetime(df['timestamp'])

# حد الكمية الآمنة (ممكن تعدله حسب رؤيتك)
threshold = 5

# تحديد الحالة: ✅ لو الكمية كافية، ❌ لو ناقصة
def get_status(row):
    if row['stock_qty'] >= threshold and row['available'] == 1:
        return "✅"
    else:
        return "❌"

df['status'] = df.apply(get_status, axis=1)

# واجهة Streamlit
st.title("📦 حالة الأدوية في المحافظات المختارة")

# اختيار المحافظة من القائمة
selected_city = st.selectbox("اختر المحافظة:", sorted(df['city'].unique()))

# تصفية البيانات حسب المحافظة
filtered_df = df[df['city'] == selected_city]

# عرض النتائج
st.dataframe(filtered_df[['pharmacy_name', 'med_name', 'stock_qty', 'status']])
# ... باقي الكود فوق كما هو ...

# تصفية البيانات حسب المحافظة المختارة
filtered_df = df[df['city'] == selected_city]

# عرض جدول البيانات
# تصفية البيانات حسب المحافظة المختارة
filtered_df = df[df['city'] == selected_city]

# تصفية الأدوية الناقصة
missing_meds = filtered_df[filtered_df['status'] == '❌']

# عرض جدول البيانات
# st.dataframe(filtered_df[['pharmacy_name', 'med_name', 'stock_qty', 'status']])

# 🔔 تنبيه لو في أدوية ناقصة
if not missing_meds.empty:
    missing_names = missing_meds['med_name'].unique().tolist()
    missing_text = "، ".join(missing_names)

    st.warning(f"⚠️ يوجد أدوية ناقصة في محافظة {selected_city}:\n\n❌ {missing_text}")
else:
    st.success(f"✅ كل الأدوية متوفرة في محافظة {selected_city}.")


query = """
SELECT 
    h.date AS holiday_date,
    h.holiday_reason,
    p.pharmacy_name,
    p.city
FROM pharmacy_holidays AS h
JOIN pharmacy_stock_new AS p
    ON h.pharmacy_id = p.pharmacy_id
ORDER BY h.date
"""

result = client.query(query)
df = pd.DataFrame(result.result_rows, columns=result.column_names)

st.title("📅 عطلات الصيدليات")
st.dataframe(df)



