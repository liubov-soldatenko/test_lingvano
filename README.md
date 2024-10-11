## Tasks

### Requirements:

Python version: Python 3.12+

Install dependency:
`pip install -r requirements.txt`

List of used python packages:
```
jupyterlab==4.2.5
pandas==2.2.3
SQLAlchemy==2.0.35
psycopg2-binary==2.9.9
```

PostgreSQL 16.x localy using docker-compose.yml:
```
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    ports:
      - 5432:5432
    volumes:
      - ~/work/postgres:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=lingvano
```

To start db locally, you need to install Docker and run:
```
docker compose up -d
```

### 1. Ingestion

This script will create table `customer_transactions` and load data using padas:
Also it will print to output all sql scripts it runs or generate:
```
python ./load_data.py
```

### 2. Basic Transformations

Remove duplicates `[remove_dups.sql](remove_dups.sql)`:
```sql
select count(*) from customer_transactions ;
-- 13082

-- The physical location of the row version within its table. 
-- Note that although the ctid can be used to locate the row version very quickly, 
-- a row's ctid will change if it is updated or moved by VACUUM FULL. 
-- Therefore ctid is useless as a long-term row identifier. A primary key should be used to identify logical rows.
DELETE FROM customer_transactions a USING (
    SELECT MIN(ctid) as ctid, order_id
    FROM customer_transactions
    GROUP BY order_id HAVING COUNT(*) > 1
) b
WHERE a.order_id = b.order_id
AND a.ctid <> b.ctid;

select count(*) from customer_transactions;
-- 13078
```

Filtering null values or test data (e.g. check user subscription ID): [filter_nulls.sql)](filter_nulls.sql)
```sql
select count(*) from customer_transactions;
-- 13078

DELETE FROM customer_transactions
WHERE user_subscription_id is NULL;

select count(*) from customer_transactions;
-- 13060
```

Data type casting ./[data_casting.py](data_casting.py):
This script read data from `customer_transactions` table and casts types and creates new table
`customer_transactions_cast`

or we can directly in original table [data_casting.sql](data_casting.sql):
```sql
UPDATE customer_transactions SET total = REPLACE(total, ',','');
UPDATE customer_transactions SET tax = REPLACE(tax, ',','');
UPDATE customer_transactions SET fee = REPLACE(fee, ',','');

ALTER TABLE customer_transactions
ALTER COLUMN total TYPE double precision USING total::double precision,
    ALTER COLUMN tax TYPE double precision USING tax::double precision,
    ALTER COLUMN fee TYPE double precision USING fee::double precision,
    ALTER COLUMN date TYPE date USING date::date;
```

### 5. Additional questions

> 1. Briefly discuss how your approach to data ingestion, transformation, and storage would change if you had 
> to implement the Medallion architecture. (max. 200-300 words)

In my case `raw ingestion` is load_data.py and it's `bronse` layer, where we load raw data from source as is.
Then using basic transformations from task 2, (e.g. remove duplicates, remove nulls, type casting and cleaning) is next
Silver layer or cleaned data.  And business level aggregation is final step ().