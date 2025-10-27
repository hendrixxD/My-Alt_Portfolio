
DROP SCHEMA IF EXISTS drv ;
CREATE SCHEMA IF NOT EXISTS drv;

-- Create drivers table and import data
CREATE TABLE IF NOT EXISTS drv.drivers_raw
(
    driver_id SERIAL PRIMARY KEY,
    name TEXT,
    city TEXT,
    signup_date TIMESTAMP,
    rating NUMERIC
);

COPY drv.drivers_raw (driver_id, name, city, signup_date, rating)
FROM '/data/drivers_raw.csv' DELIMITER ',' CSV HEADER;

---
CREATE TABLE IF NOT EXISTS drv.payments_raw
(
    payment_id SERIAL PRIMARY KEY,
    ride_id INTEGER,
    amount NUMERIC,
    method TEXT,
    paid_date TIMESTAMP
);

COPY drv.payments_raw (payment_id, ride_id, amount, method, paid_date)
FROM '/data/payments_raw.csv' DELIMITER ',' CSV HEADER;

---
CREATE TABLE IF NOT EXISTS drv.riders_raw
(
    rider_id SERIAL PRIMARY KEY,
    name TEXT,
    signup_date TIMESTAMP,
    city TEXT,
    email TEXT
);

COPY drv.riders_raw (rider_id, name, signup_date, city, email)
FROM '/data/riders_raw.csv' DELIMITER ',' CSV HEADER;

---
CREATE TABLE IF NOT EXISTS drv.rides_raws
(
    ride_id SERIAL PRIMARY KEY,
    rider_id INTEGER,
    driver_id INTEGER,
    request_time TIMESTAMP,
    pickup_time TIMESTAMP,
    dropoff_time TIMESTAMP,
    pickup_city TEXT,
    dropoff_city TEXT,
    distance_km NUMERIC,
    status TEXT,
    fare NUMERIC
);

COPY drv.rides_raws (ride_id, rider_id, driver_id, request_time, pickup_time, dropoff_time, pickup_city, dropoff_city, distance_km, status, fare)
FROM '/data/rides_raw.csv' DELIMITER ',' CSV HEADER;