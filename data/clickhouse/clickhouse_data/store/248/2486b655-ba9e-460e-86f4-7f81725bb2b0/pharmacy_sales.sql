ATTACH TABLE _ UUID '4704bcf4-1ea1-48a8-871b-f1bfa21922bc'
(
    `sale_id` Int32,
    `pharmacy_id` Int32,
    `med_code` Int32,
    `quantity` Int32,
    `sale_amount` Float32,
    `timestamp` DateTime
)
ENGINE = MergeTree
ORDER BY timestamp
SETTINGS index_granularity = 8192
