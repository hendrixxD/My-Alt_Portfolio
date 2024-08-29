-- What was the monthly total quantity purchased and sold for Ethereum in 2020? Your
-- query should return exactly three columns - calendar_month, buy_qunatity,
-- sell_quantity

SELECT
	EXTRACT(MONTH FROM txn_date::DATE) AS calendar_month,
	SUM(CASE
			WHEN txn_type = 'BUY'
			THEN quantity ELSE 0
		END
	) AS buy_quantity,
	SUM(CASE
			WHEN txn_type = 'SELL'
			THEN quantity ELSE 0
		END
	) AS sell_quantity
FROM
	raw.transactions
WHERE
	ticker = 'ETH'
	AND EXTRACT(YEAR FROM txn_date::DATE) = 2020
GROUP BY
	calendar_month
ORDER BY
	calendar_month;
