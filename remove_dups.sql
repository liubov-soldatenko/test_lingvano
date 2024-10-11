select count(*) from customer_transactions ;
-- 13082
-- The physical location of the row version within its table. Note that although the ctid can be used to locate the row version very quickly, a row's ctid will change if it is updated or moved by VACUUM FULL. Therefore ctid is useless as a long-term row identifier. A primary key should be used to identify logical rows.
DELETE FROM customer_transactions a USING (
    SELECT MIN(ctid) as ctid, order_id
    FROM customer_transactions
    GROUP BY order_id HAVING COUNT(*) > 1
) b
WHERE a.order_id = b.order_id
AND a.ctid <> b.ctid;

select count(*) from customer_transactions;
-- 13078