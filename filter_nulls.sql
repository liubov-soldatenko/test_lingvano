select count(*) from customer_transactions;
-- 13078

DELETE FROM customer_transactions
WHERE user_subscription_id is NULL;

select count(*) from customer_transactions;
-- 13060


