UPDATE customer_transactions SET total = REPLACE(total, ',','');
UPDATE customer_transactions SET tax = REPLACE(tax, ',','');
UPDATE customer_transactions SET fee = REPLACE(fee, ',','');

ALTER TABLE customer_transactions
    ALTER COLUMN total TYPE double precision USING total::double precision,
    ALTER COLUMN tax TYPE double precision USING tax::double precision,
    ALTER COLUMN fee TYPE double precision USING fee::double precision,
    ALTER COLUMN date TYPE date USING date::date;


