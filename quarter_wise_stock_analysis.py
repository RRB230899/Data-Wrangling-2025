import pandas as pd
import matplotlib.pyplot as plt

# Load the quarterly stock data
stock_df = pd.read_csv("tsmc_quarterly_stock_prices.csv")

# Drop NA and ensure the data is sorted
stock_df = stock_df.dropna(subset=["q", "Close"])
stock_df = stock_df.sort_values("q")

# Calculate percent change in Close price by quarter
stock_df["pct_change"] = stock_df["Close"].pct_change() * 100

# Define significant movement threshold
threshold = 15  # 15% up or down


# Label the movement
def classify_change(pct):
    if pct > threshold:
        return "Significant Rise"
    elif pct < -threshold:
        return "Significant Drop"
    else:
        return "Stable"


stock_df["Movement"] = stock_df["pct_change"].apply(classify_change)

# Plotting
plt.figure(figsize=(14, 6))
bars = plt.bar(stock_df["q"], stock_df["pct_change"], color=stock_df["Movement"].map({
    "Significant Rise": "green",
    "Significant Drop": "red",
    "Stable": "gray"
}))
plt.axhline(y=15, color='blue', linestyle='--', linewidth=1, label='±15% Threshold')
plt.axhline(y=-15, color='blue', linestyle='--', linewidth=1)
plt.xticks(rotation=45)
plt.ylabel("% Change in Close Price")
plt.title("Quarterly % Change in TSMC Stock Closing Price")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()
