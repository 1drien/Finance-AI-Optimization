import numpy as np
import pandas as pd 
import matplotlib
matplotlib.use('Agg')   # Backend for non-GUI environments (saves files instead of showing them)
import matplotlib.pyplot as plt

# --- 1. Load Data ---
# Reading the dataset
try:
    df = pd.read_csv('apple2122.csv')
    df["Date"] = pd.to_datetime(df["Date"])
    print("Data loaded successfully.")
    print(df.head())
except FileNotFoundError:
    print("Error: 'apple2122.csv' not found. Please make sure the file is in the same directory.")
    exit()

# --- 2. Moving Averages Calculation ---
# Calculating Short (20 days) and Long (50 days) Moving Averages
df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()

# Plotting the price and Moving Averages
plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Close"], label="Close Price", alpha=0.5)
plt.plot(df["Date"], df["MA20"], label="MA 20 Days")
plt.plot(df["Date"], df["MA50"], label="MA 50 Days")
plt.legend()
plt.title("Apple Stock Price & Moving Averages")
plt.grid(True)
plt.savefig("ma_analysis.png")
print("Saved moving average plot to 'ma_analysis.png'")

# --- 3. Signal Generation ---
# Strategy: Bullish (1) if MA20 > MA50, else Bearish (-1)
df["signal"] = np.where(df["MA20"] > df["MA50"], 1, -1)

# Identify trade triggers (differences between signals)
df["trade"] = df["signal"].diff()

# Define Buy (2) and Sell (-2) signals based on the crossover
df["buy_signal"] = np.where(df["trade"] == 2, 1, 0)
df["sell_signal"] = np.where(df["trade"] == -2, 1, 0)

print("Recent signals generated:")
print(df[["Date", "Close", "buy_signal", "sell_signal"]].tail(10))

# --- 4. Portfolio Simulation (Backtesting) ---
initial_capital = 100000.0
share_quantity = 100

# Initialize portfolio columns
df["cash"] = initial_capital
df["positions"] = 0 

print("Starting portfolio simulation...")

# Iterate through each day to simulate the strategy
for i in range(1, len(df)):
    
    # 1. Carry over previous day's state
    df.loc[i, "cash"] = df.loc[i-1, "cash"]
    df.loc[i, "positions"] = df.loc[i-1, "positions"]

    # 2. Check for trade signals
    current_price = df.loc[i, "Close"]
    
    # Buy Signal
    if df.loc[i, "buy_signal"] == 1:
        # Check if we have enough cash (optional safeguard, simplified here)
        df.loc[i, "positions"] += share_quantity
        df.loc[i, "cash"] -= share_quantity * current_price
        
    # Sell Signal
    elif df.loc[i, "sell_signal"] == 1:
        # Check if we have shares to sell (optional safeguard)
        if df.loc[i, "positions"] >= share_quantity:
            df.loc[i, "positions"] -= share_quantity
            df.loc[i, "cash"] += share_quantity * current_price

# Calculate Total Portfolio Value (Cash + Asset Value)
df["portfolio_value"] = df["cash"] + (df["positions"] * df["Close"])

# --- 5. Visualization & Results ---
plt.figure(figsize=(12, 6))

# Plot Portfolio Value
plt.plot(df["Date"], df["portfolio_value"], label="Portfolio Value (MA Strategy)", color='blue', linewidth=1.5)

# Plot Baseline (Initial Capital)
plt.axhline(y=initial_capital, color='r', linestyle='--', label="Initial Capital ($100k)")

# Formatting
plt.title("Portfolio Evolution - MA Crossover Strategy", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Total Value ($)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Save final result
plt.savefig("portfolio_evolution.png")
print("Simulation complete. Graph saved to 'portfolio_evolution.png'")
print(f"Final Portfolio Value: ${df['portfolio_value'].iloc[-1]:,.2f}")