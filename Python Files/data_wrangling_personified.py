# Remove QuarterLocator since it's not necessary for this plot

import pandas as pd
import matplotlib.pyplot as plt

# Load the stock price data
stock_df = pd.read_csv("tsmc_quarterly_stock_prices.csv")
stock_df["Date"] = pd.to_datetime(stock_df["Date"])
stock_df["Quarter"] = stock_df["q"]

# Compute quarterly percent change in stock price
stock_df["Pct_Change"] = stock_df["Close"].pct_change() * 100

# Identify significant spikes and dips
threshold = 10  # percent
stock_df["Movement"] = stock_df["Pct_Change"].apply(
    lambda x: "Spike" if x > threshold else ("Dip" if x < -threshold else "Stable")
)

# Plot
plt.figure(figsize=(14, 6))
plt.plot(stock_df["Date"], stock_df["Close"], marker='o', label="Stock Price")
plt.title("TSMC Quarterly Stock Prices with Spikes and Dips Highlighted")
plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")

# Highlight spikes and dips
spike_points = stock_df[stock_df["Movement"] == "Spike"]
dip_points = stock_df[stock_df["Movement"] == "Dip"]
plt.scatter(spike_points["Date"], spike_points["Close"], color='green', label='Spike', s=100, marker='^')
plt.scatter(dip_points["Date"], dip_points["Close"], color='red', label='Dip', s=100, marker='v')

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()

# Return the key spike/dip events for analysis
print(stock_df[stock_df["Movement"] != "Stable"][["Quarter", "Close", "Pct_Change", "Movement"]])
