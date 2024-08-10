# -*- coding: utf-8 -*-
"""Quantitative Finance week 1 assign1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/197m8E15crMAGYobCOX-zMHNal3Q69B8W

Question 1:

Write a Python script to analyze historical stock data for a NIFTY50 stock from Yahoo Finance for the period from August 1, 2022, to August 1, 2024. The script should:

Install the necessary libraries (numpy, pandas, yfinance, matplotlib).
Download the data for the given period.
Extract the Open, High, Low, Close, Adj Close, and Volume columns.
Calculate and plot the 14-day and 50-day relative strength index (RSI) on the same graph, with different colors for each RSI.
Compute and visualize the daily percentage change in the Closing Prices and plot it as a histogram with appropriate bins.
Create a subplot with three charts:
The first chart should display the daily Closing Prices with 14-day and 50-day RSI.
The second chart should show the daily Volume.
The third chart should display the histogram of daily percentage changes.
"""

# Install necessary libraries
!pip install numpy
!pip install pandas
!pip install yfinance
!pip install matplotlib

# Import libraries
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock ticker and date range
ticker=yf.Ticker('RELIANCE.NS')
start_date='2022-08-01'
end_date='2024-08-01'

# Download historical stock data
stock_data = ticker.history(start=start_date, end=end_date)

# Extract the relevant columns
stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]

# Define function to calculate RSI
def calculate_rsi(data, window):
    delta = data['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Calculate the 14-day and 50-day relative strength index (RSI)
stock_data['RSI_14'] = calculate_rsi(stock_data, 14)
stock_data['RSI_50'] = calculate_rsi(stock_data, 50)

# Calculate the daily percentage change in Closing Prices
stock_data['Daily Change'] = stock_data['Close'].pct_change() * 100

# Create subplots
plt.figure(figsize=(14, 12))

# Plot Closing Prices and RSI
plt.subplot(3, 1, 1)
plt.plot(stock_data.index, stock_data['Close'], label='Closing Price', color='blue')
plt.plot(stock_data.index, stock_data['RSI_14'], label='14-Day RSI', color='green')
plt.plot(stock_data.index, stock_data['RSI_50'], label='50-Day RSI', color='red')
plt.title("RELIANCE.NS Closing Prices and RSI")
plt.xlabel('Date')
plt.ylabel('Price / RSI')
plt.legend()
plt.grid()

# Plot Volume
plt.subplot(3, 1, 2)
plt.bar(stock_data.index, stock_data['Volume'], color='purple')
plt.title("RELIANCE.NS Daily Volume")
plt.xlabel('Date')
plt.ylabel('Volume')
plt.grid()

# Plot histogram of daily percentage changes
plt.subplot(3, 1, 3)
plt.hist(stock_data['Daily Change'].dropna(), bins=50, color='orange', edgecolor='black')
plt.title("RELIANCE.NS Daily Percentage Change Histogram")
plt.xlabel('Percentage Change (%)')
plt.ylabel('Frequency')
plt.grid()

plt.tight_layout()
plt.show()