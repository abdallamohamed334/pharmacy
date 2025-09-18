CREATE TABLE pharmacy_stock
(
    pharmacy_id Int32,
    pharmacy_name String,
    city String,
    med_name String,
    med_code Int32,
    available UInt8,  -- لأن ClickHouse ما عندوش Boolean، نستخدم UInt8 (0 or 1)
    stock_qty Int32,
    timestamp DateTime
)
ENGINE = MergeTree
ORDER BY timestamp;



CREATE TABLE pharmacy_sales (
    sale_id Int32,
    pharmacy_id Int32,
    med_code Int32,
    quantity Int32,
    sale_amount Float32,
    timestamp DateTime
)
ENGINE = MergeTree
ORDER BY (timestamp);


CREATE TABLE pharmacy_stock_new (
    pharmacy_id Int32,
    pharmacy_name String,
    city String,
    med_name String,
    med_code Int32,
    available UInt8,
    stock_qty Int32,
    timestamp DateTime64(3)  -- دعم ثواني مع دقة 3 أرقام عشرية (مللي ثانية)
) 
ENGINE = MergeTree()
ORDER BY pharmacy_id;

DROP TABLE IF EXISTS pharmacy_stock_new;



CREATE TABLE pharmacy_stock_new (
    pharmacy_id Int32,
    pharmacy_name String,
    city String,
    med_name String,
    med_code Int32,
    available UInt8,
    stock_qty Int32,
    timestamp DateTime64(3)
)
ENGINE = MergeTree()
ORDER BY pharmacy_id;


select version()



CREATE TABLE IF NOT EXISTS pharmacy_sales (
    pharmacy_id Int32,
    med_code Int32,
    date Date,
    units_sold Int32
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (pharmacy_id, med_code, date);

CREATE TABLE IF NOT EXISTS pharmacy_holidays (
    pharmacy_id Int32,
    date Date,
    holiday_reason String
) 
ENGINE = MergeTree()
ORDER BY pharmacy_id;


INSERT INTO pharmacy_holidays (pharmacy_id, date, holiday_reason) VALUES
(113, '2025-09-11', 'ظرف طارئ'),
(123, '2025-09-18', 'صيانة داخلية'),
(133, '2025-09-12', 'صيانة داخلية'),
(143, '2025-09-20', 'مشكلة كهرباء'),
(153, '2025-09-05', 'ظرف طارئ'),
(163, '2025-09-23', 'ظرف طارئ'),
(123, '2025-09-14', 'إجازة رسمية'),
(193, '2025-09-13', 'إجازة رسمية');

