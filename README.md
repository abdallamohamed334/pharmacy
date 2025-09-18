# 🏥 Pharmacy Data Pipeline Project  

## 📌 Overview  
This project is a **Big Data pipeline** designed to monitor and analyze pharmacy and drug data across different regions.  
It combines **Batch Processing** and **Real-time Streaming** to provide:  
- 📊 **Real-time Dashboards** for instant monitoring.  
- 📈 **Historical Analytics** for long-term insights.  

---

## 🎯 Objectives  
- 🔎 Monitor **drug availability** across pharmacies in real-time.  
- 🚨 Detect **shortages, failures, or anomalies** instantly.  
- 📂 Provide **historical dashboards** for batch analysis.  
- 📢 Send **alerts** when critical issues occur (drug shortages, pharmacy outages).  

---

## 🛠️ Tech Stack  

### 🔹 Data Ingestion  
- ⚡ **Apache Kafka** → Real-time streaming.  
- 🔥 **Apache Spark** → Batch & Stream processing.  

### 🔹 Data Storage  
- 🗄️ **HDFS** → Raw storage (Batch + Streaming archive).  
- ⚡ **ClickHouse** → High-performance analytics DB.  
- 🐘 **PostgreSQL** → Relational database for batch analytics.  

### 🔹 Visualization & Alerts  
- 📊 **Streamlit** → Real-time dashboards.  
- 📈 **Grafana** → Batch analytics dashboards.  
- 📢 **Custom Python Alerts** → Notifications for shortages & failures.  

### 🔹 Language  
- 🐍 **Python**  

---

## 🔄 Architecture  

![Architecture Diagram](pharmacy.drawio.png)  

---

## 📊 Features  

✅ **Real-time Monitoring (Streamlit)**  
- Current stock levels by pharmacy/region.  
- Shortage & outage detection.  
- Instant alerts for missing drugs.  

✅ **Batch Analytics (Grafana)**  
- Long-term drug consumption trends.  
- Regional comparison of pharmacies.  
- Top-selling drugs & historical patterns.  

---

## 🚀 Getting Started  

### 1️⃣ Start Required Services  
Ensure **Kafka, Spark, HDFS, ClickHouse, PostgreSQL** are running. (Docker Compose recommended).  

### 2️⃣ Generate Fake Data  
```bash
python data_generator.py
