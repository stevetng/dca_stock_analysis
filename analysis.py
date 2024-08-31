import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize lists to store portfolio values
strategy_portfolio_values = []
buyhold_portfolio_values = []

# Load the data
df = pd.read_csv('SPY_30_years.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Calculate moving averages
df['50_MA'] = df['Close'].rolling(window=50).mean()
df['200_MA'] = df['Close'].rolling(window=200).mean()

# Initialize variables for strategy
base_amount = 500
strategy_portfolio_value = 0
strategy_shares = 0
strategy_total_invested = 0

# Initialize variables for buy-and-hold
buyhold_portfolio_value = 0
buyhold_shares = 0
buyhold_total_invested = 0

# Apply the strategies
for index, row in df.iterrows():
    if pd.notna(row['50_MA']) and pd.notna(row['200_MA']):
        # Strategy investment
        if row['Close'] > row['50_MA'] * 1.05:
            investment = base_amount / 2
        elif row['200_MA'] < row['Close'] <= row['50_MA']:
            investment = base_amount
        elif row['Close'] <= row['200_MA']:
            investment = base_amount * 1.5
        else:
            investment = base_amount

        strategy_shares_bought = investment / row['Close']
        strategy_shares += strategy_shares_bought
        strategy_total_invested += investment

        # Buy-and-hold investment
        buyhold_shares_bought = base_amount / row['Close']
        buyhold_shares += buyhold_shares_bought
        buyhold_total_invested += base_amount

    strategy_portfolio_value = strategy_shares * row['Close']
    buyhold_portfolio_value = buyhold_shares * row['Close']
    
    # Append the portfolio values to the lists
    strategy_portfolio_values.append(strategy_portfolio_value)
    buyhold_portfolio_values.append(buyhold_portfolio_value)

# Calculate returns
strategy_return = (strategy_portfolio_value - strategy_total_invested) / strategy_total_invested * 100
buyhold_return = (buyhold_portfolio_value - buyhold_total_invested) / buyhold_total_invested * 100

# Calculate CAGR (Compound Annual Growth Rate)
years = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days / 365.25
strategy_cagr = (strategy_portfolio_value / strategy_total_invested) ** (1/years) - 1
buyhold_cagr = (buyhold_portfolio_value / buyhold_total_invested) ** (1/years) - 1

print(f"Strategy Final Portfolio Value: ${strategy_portfolio_value:,.2f}")
print(f"Strategy Total Invested: ${strategy_total_invested:,.2f}")
print(f"Strategy Return: {strategy_return:.2f}%")
print(f"Strategy CAGR: {strategy_cagr:.2f}%")
print(f"\nBuy-and-Hold Final Portfolio Value: ${buyhold_portfolio_value:,.2f}")
print(f"Buy-and-Hold Total Invested: ${buyhold_total_invested:,.2f}")
print(f"Buy-and-Hold Return: {buyhold_return:.2f}%")
print(f"Buy-and-Hold CAGR: {buyhold_cagr:.2f}%")
print(f"\nStrategy Outperformance: {strategy_return - buyhold_return:.2f}%")
print(f"Strategy CAGR Outperformance: {(strategy_cagr - buyhold_cagr) * 100:.2f}%")

# Plot the returns
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], strategy_portfolio_values, label='Strategy')
plt.plot(df['Date'], buyhold_portfolio_values, label='Buy and Hold')
plt.title('Portfolio Value Comparison')
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.legend()
plt.grid(True)
plt.show()

# Plot the returns (log scale)
plt.figure(figsize=(12, 6))
plt.semilogy(df['Date'], strategy_portfolio_values, label='Strategy')
plt.semilogy(df['Date'], buyhold_portfolio_values, label='Buy and Hold')
plt.title('Portfolio Value Comparison (Log Scale)')
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.legend()
plt.grid(True)
plt.show()