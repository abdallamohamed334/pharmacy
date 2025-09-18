ATTACH TABLE _ UUID 'f4aafd89-6b99-4b88-bfbf-cc912c1adb04'
(
    `pharmacy_id` Int32,
    `pharmacy_name` String,
    `city` String,
    `med_name` String,
    `med_code` Int32,
    `available` UInt8,
    `stock_qty` Int32,
    `timestamp` DateTime64(3)
)
ENGINE = MergeTree
ORDER BY pharmacy_id
SETTINGS index_granularity = 8192
