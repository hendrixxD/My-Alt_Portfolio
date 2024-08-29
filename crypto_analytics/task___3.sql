-- What was the monthly total quantity purchased and sold for Ethereum in 2020? Your
-- query should return exactly three columns - calendar_month, buy_qunatity,
-- sell_quantity

select
	EXTRACT(MONTH FROM market_date::DATE) calender_month,
	SUM(CASE WHEN price >= open THEN REGEXP_REPLACE(volume, '[^0-9.]', '', 'g')::NUMERIC ELSE 0 END) buy_quantity,
	SUM(CASE WHERE price < open THEN REGEXP_REPLACE(volume, '[^0-9.]', '', 'g')::NUMERIC ELSE 0 END) sell_quantity
FROM
	raw.prices
WHERE
	ticker = 'ETH'
	AND EXTRACT(YEAR FROM market_date::DATE) = 2020
GROUP BY
	calender_month
ORDER By
   calender_month;