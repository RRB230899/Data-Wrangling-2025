import pandas as pd
import yfinance as yf

df = pd.read_csv("lamini_earnings_calls_all.csv")

# Filter: exact case-insensitive match in question or answer
df_tsmc = df[
    df["question"].str.contains("TSMC", case=False, na=False) |
    df["answer"].str.contains("TSMC", case=False, na=False) |
    df["transcript"].str.contains("TSMC", case=False, na=False)
]

# Save filtered data
df_tsmc.to_csv("tsmc_earnings_calls_filtered.csv", index=False)
print(f"✅ Found {len(df_tsmc)} TSMC-related earnings Q&A entries.")

# === PART 2: DOWNLOAD TSMC STOCK DATA FROM YAHOO FINANCE ===
print("\nDownloading quarterly stock price data for TSMC...")
ts = yf.Ticker("TSM")
ts_data = ts.history(period="5y", interval="3mo")
ts_data.to_csv("tsmc_quarterly_stock_prices.csv")
print("✅ Stock price data saved to 'tsmc_quarterly_stock_prices.csv'")
