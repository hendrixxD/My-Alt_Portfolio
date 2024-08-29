-- How many buy and sell transactions are there for Bitcoin? - 
-- your result should return two columns - txn_type, transaction_count

SELECT
	txn_type,
	COUNT(quantity) AS transaction_count
FROM
	raw.transactions
WHERE
	ticker = 'BTC'
GROUP BY
	txn_type;
