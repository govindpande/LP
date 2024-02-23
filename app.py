import streamlit as st
import numpy as np
import yfinance as yf
from scipy.stats import norm

# Fetch stock data
def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    last_close = hist['Close'][-1]
    return last_close

# Black-Scholes formula
def black_scholes(S, X, T, r, sigma, option_type='call'):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        option_price = (S * norm.cdf(d1, 0.0, 1.0) - X * np.exp(-r * T) * norm.cdf(d2, 0.0, 1.0))
    elif option_type == 'put':
        option_price = (X * np.exp(-r * T) * norm.cdf(-d2, 0.0, 1.0) - S * norm.cdf(-d1, 0.0, 1.0))
    
    return option_price

# Streamlit interface
st.title('Black-Scholes Option Pricing Calculator with Live Data')

ticker = st.text_input('Enter Stock Ticker (e.g., AAPL, GOOG)', value='AAPL').upper()
fetch = st.button('Fetch Current Stock Price')

if fetch:
    try:
        current_price = fetch_data(ticker)
        st.success(f"Current Price for {ticker}: {current_price}")
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {str(e)}")
        current_price = 0
else:
    current_price = 0

X = st.number_input('Strike Price (X)', value=100.0)
T = st.slider('Time to Maturity (T) in years', 0.01, 2.0, 1.0)
r = st.slider('Risk-Free Interest Rate (r)', 0.01, 0.1, 0.05)
sigma = st.slider('Volatility of the Stock Returns (σ)', 0.1, 1.0, 0.2)
option_type = st.selectbox('Option Type', ['call', 'put'])

if st.button('Calculate Option Price') and current_price > 0:
    option_price = black_scholes(current_price, X, T, r, sigma, option_type)
    st.write(f"The {option_type} option price for {ticker} is: {option_price:.2f}")
else:
    st.write("Enter all parameters to calculate the option price.")
