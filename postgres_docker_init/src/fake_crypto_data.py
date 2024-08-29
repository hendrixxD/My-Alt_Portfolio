import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


random.seed(0)
np.random.seed(0)


def generate_fake_data(num_records):
    data = []

    tickers = ['BTC', 'ETH', 'LTC', 'XRP', 'ADA']
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365*2)

    for _ in range(num_records):
        ticker = random.choice(tickers)
        market_date = start_date + timedelta(days=random.randint(0, 365*2))
        open_price = round(random.uniform(100, 50000), 2)
        high = round(open_price + random.uniform(0, 1000), 2)
        low = round(open_price - random.uniform(0, 1000), 2)
        price = round(random.uniform(low, high), 2)
        volume = round(random.uniform(10000, 1000000), 2)
        change = round((price - open_price) / open_price * 100, 2)
        market_cap = round(price * random.uniform(1e6, 1e9), 2)
        circulating_supply = round(random.uniform(1e6, 1e9), 2)
        percent_change_24h = round(random.uniform(-20, 20), 2)
        percent_change_7d = round(random.uniform(-50, 50), 2)

        data.append([ticker, market_date.strftime('%Y-%m-%d'), price, open_price, high, low, volume, f"{change}%", market_cap, circulating_supply, percent_change_24h, percent_change_7d])

    return pd.DataFrame(data, columns=['ticker', 'market_date', 'price', 'open_price', 'high', 'low', 'volume', 'change', 'market_cap', 'circulating_supply', 'percent_change_24h', 'percent_change_7d'])


# Generate 1000 fake data records
df = generate_fake_data(1000)

# Saves data to CSV
df.to_csv('./data/fake_crypto_data.csv', index=False)

# Display the first few rows
print(df.head())
