import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.api as sm
import plotly.express as px
import datetime

# Page Configuration
st.set_page_config(page_title="CAPM Beta Calculator", page_icon="📊", layout="wide")
st.title("CAPM Beta Calculator")
# Display description about what the website provides
# st.write("""
#     **CAPM Beta Calculator** helps you analyze the performance of a stock in relation to a market index. 
#     The key features of this tool include:
    
#     - **Beta**: Measures a stock's volatility relative to the market.
#     - **Alpha**: Shows how well the stock has performed relative to the expected return.
#     - **Stock vs. Market Scatter Plot**: Visualizes the relationship between stock and market returns.
#     - **Rolling Beta**: Tracks stock volatility over time.
#     - **Sector Beta Comparison**: Compare the Beta values of popular sector stocks (e.g., Tech sector).
#     - **Sharpe Ratio**: Assesses risk-adjusted return by comparing the stock's performance to a risk-free rate.
    
#     You can input stock tickers and market index tickers, choose the analysis period, and adjust settings to explore the stock's risk and performance.
# """)

# Sidebar with additional information
st.sidebar.header("About CAPM Beta Calculator")
st.sidebar.write("""
    The CAPM (Capital Asset Pricing Model) Beta Calculator allows you to:
    
    - Calculate the **Beta** and **Alpha** of a stock relative to a market index.
    - Visualize stock vs. market returns with a scatter plot.
    - Analyze rolling Beta to track changes in stock volatility over time.
    - Compare the **Beta** values of popular sector stocks.
    - Assess **Sharpe Ratio** for risk-adjusted performance.
    
    **What is Beta?**
    Beta measures a stock's volatility relative to the market. A Beta greater than 1 indicates a stock is more volatile than the market, while a Beta less than 1 indicates it is less volatile.
""")

st.sidebar.header("Instructions")
st.sidebar.write("""
    1. Enter the stock ticker you want to analyze (e.g., TSLA for Tesla).
    2. Choose the market index ticker (e.g., ^GSPC for the S&P 500).
    3. Select the start and end dates for the analysis.
    4. Adjust the rolling window to calculate rolling Beta.
    5. View various charts and metrics to better understand the stock's performance.
""")

# Column layout for inputs
col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    stock_ticker = st.text_input("Stock Ticker", "TSLA")
with col2:
    market_ticker = st.text_input("Market Index Ticker (e.g., ^GSPC for S&P 500)", "^GSPC")
with col3:
    start_date = st.date_input("Start Date", datetime.date(today.year - 1, today.month, today.day))
    end_date = st.date_input("End Date", today)

# Fetch Stock & Market Data
stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
market_data = yf.download(market_ticker, start=start_date, end=end_date)

# Ensure data has 'Adj Close' or fall back to 'Close'
if 'Adj Close' in stock_data.columns:
    stock_data["Stock Return"] = stock_data["Adj Close"].pct_change()
else:
    if 'Close' in stock_data.columns:
        stock_data["Stock Return"] = stock_data["Close"].pct_change()
    else:
        st.error("Neither 'Adj Close' nor 'Close' columns are available in the stock data.")
        st.stop()

if 'Adj Close' in market_data.columns:
    market_data["Market Return"] = market_data["Adj Close"].pct_change()
else:
    if 'Close' in market_data.columns:
        market_data["Market Return"] = market_data["Close"].pct_change()
    else:
        st.error("Neither 'Adj Close' nor 'Close' columns are available in the market data.")
        st.stop()

# Drop NaN values
data = pd.merge(stock_data["Stock Return"], market_data["Market Return"], left_index=True, right_index=True).dropna()

# CAPM Regression (OLS)
X = sm.add_constant(data["Market Return"])  # Add constant for intercept
y = data["Stock Return"]
model = sm.OLS(y, X).fit()
beta = model.params.iloc[1]  # Beta coefficient
alpha = model.params.iloc[0]  # Alpha coefficient

# Display Beta & Alpha Values
st.subheader(f"Beta Value for {stock_ticker}: **{round(beta, 3)}**")
st.subheader(f"Alpha Value for {stock_ticker}: **{round(alpha, 3)}**")

# Scatter Plot of Returns
fig = px.scatter(data, x="Market Return", y="Stock Return", trendline="ols",
                 title=f"Stock vs. Market Returns ({stock_ticker} vs {market_ticker})")
st.plotly_chart(fig, use_container_width=True)

# Rolling Beta Calculation
rolling_window = st.slider("Select Rolling Window (days)", min_value=30, max_value=365, value=180, step=30)

rolling_beta = data["Stock Return"].rolling(rolling_window).cov(data["Market Return"]) / \
               data["Market Return"].rolling(rolling_window).var()

st.subheader("Rolling Beta Over Time")
st.line_chart(rolling_beta.dropna(), use_container_width=True)

# Sector Beta Comparison
st.subheader("Sector Beta Comparison")

sector_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  # Example tech sector stocks
sector_betas = {}

for ticker in sector_tickers:
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data["Return"] = stock_data["Adj Close"].pct_change() if "Adj Close" in stock_data.columns else stock_data["Close"].pct_change()
    data_comp = pd.merge(stock_data["Return"], market_data["Market Return"], left_index=True, right_index=True).dropna()
    
    if not data_comp.empty:
        X_comp = sm.add_constant(data_comp["Market Return"])
        y_comp = data_comp["Return"]
        model_comp = sm.OLS(y_comp, X_comp).fit()
        sector_betas[ticker] = model_comp.params.iloc[1]

st.bar_chart(pd.Series(sector_betas))

# Risk-Adjusted Performance (Sharpe Ratio)
st.subheader("Sharpe Ratio")

risk_free_rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, max_value=10.0, value=2.0) / 100
excess_return = data["Stock Return"].mean() - risk_free_rate
volatility = data["Stock Return"].std()

sharpe_ratio = excess_return / volatility
st.subheader(f"Sharpe Ratio: **{round(sharpe_ratio, 3)}**")

# Show Regression Summary
with st.expander("View Regression Summary"):
    st.text(model.summary())

# Interpretation
st.write("**Interpretation:**")
st.write("🔹 **Beta > 1:** Stock is more volatile than the market (aggressive stock).")
st.write("🔹 **Beta < 1:** Stock is less volatile than the market (defensive stock).")
st.write("🔹 **Beta ≈ 1:** Stock moves similarly to the market.")
st.write("🔹 **Alpha > 0:** Stock outperforms the market.")
st.write("🔹 **Alpha < 0:** Stock underperforms the market.")
st.write("🔹 **Sharpe Ratio > 1:** Indicates a good risk-adjusted return.")
