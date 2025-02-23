import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
import numpy as np

# Monkey patch: ensure np.NaN exists (fix for pandas_ta compatibility with latest NumPy)
if not hasattr(np, 'NaN'):
    np.NaN = np.nan

from pages.utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, MACD, Moving_average_forecast
import plotly.io as pio

# Setting page configuration
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="🔍",
    layout="wide"
)

st.title("Stock Analysis")

# Sidebar for app information
st.sidebar.title("About the App")
st.sidebar.subheader("Stock Analysis App")
st.sidebar.write(
    """
    This app allows you to analyze stock data using Yahoo Finance. You can view company information, historical stock data, and technical indicators such as RSI, MACD, and Moving Averages.
    """
)
st.sidebar.subheader("Features")
st.sidebar.write(
    """
    - View stock information such as market cap, PE ratio, and revenue per share.
    - Display stock data for selected periods.
    - Plot candlestick charts and line charts with technical indicators like RSI, MACD, and Moving Averages.
    """
)
st.sidebar.subheader("Data Source")
st.sidebar.write("The stock data is sourced from Yahoo Finance using the yfinance package.")
st.sidebar.subheader("Technical Indicators")
st.sidebar.write(
    """
    - **RSI (Relative Strength Index)**: A momentum oscillator that measures the speed and change of price movements.
    - **MACD (Moving Average Convergence Divergence)**: A trend-following momentum indicator that shows the relationship between two moving averages of a stock's price.
    - **Moving Averages**: A widely-used technical indicator to smooth price data and identify trends.
    """
)

# Main content: define three columns for ticker and date inputs
col1, col2, col3 = st.columns(3)
today = datetime.date.today()

with col1:
    ticker_input = st.text_input("Stock Ticker", "TSLA")
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", today)

st.subheader(ticker_input)

# Fetch stock data using yfinance
stock = yf.Ticker(ticker_input)

# Display company information if available
if "longBusinessSummary" in stock.info:
    st.write(stock.info["longBusinessSummary"])
st.write("**Sector:**", stock.info.get("sector", "N/A"))
st.write("**Full Time Employees:**", stock.info.get("fullTimeEmployees", "N/A"))
st.write("**Website:**", stock.info.get("website", "N/A"))

col1, col2 = st.columns(2)

with col1:
    # Create DataFrame for key stock data
    df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [
        stock.info.get("marketCap", "N/A"),
        stock.info.get("beta", "N/A"),
        stock.info.get("trailingEps", "N/A"),
        stock.info.get("trailingPE", "N/A")
    ]
    fig = plotly_table(df)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Create DataFrame for additional stock data
    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
    df[''] = [
        stock.info.get("quickRatio", "N/A"),
        stock.info.get("revenuePerShare", "N/A"),
        stock.info.get("profitMargins", "N/A"),
        stock.info.get("debtToEquity", "N/A"),
        stock.info.get("returnOnEquity", "N/A")
    ]
    fig = plotly_table(df)
    st.plotly_chart(fig, use_container_width=True)

# Display dividend information if available
if not stock.dividends.empty:
    st.subheader('Dividends')
    dividend_data = stock.dividends
    st.write(dividend_data)

# Download historical stock data
data = yf.download(ticker_input, start=start_date, end=end_date)

col1, col2, col3 = st.columns(3)
# Calculate last close price and daily change
last_close_price = data['Close'].iloc[-1].item()
daily_change_value = (data['Close'].iloc[-1] - data['Close'].iloc[-2]).item()
col1.metric("Daily Change", str(round(last_close_price, 2)), str(round(daily_change_value, 2)))

# Display last 10 days of historical data as a table
last_10_df = data.tail(10).sort_index(ascending=False).round(3)
if isinstance(last_10_df.columns, pd.MultiIndex):
    last_10_df.columns = [' '.join(col).strip() for col in last_10_df.columns.values]
last_10_df.columns = last_10_df.columns.str.replace(ticker_input, '', regex=False)
fig = plotly_table(last_10_df)
st.write('##### Historical Data (Last 10 days)')
st.plotly_chart(fig, use_container_width=True)

# Buttons for selecting time period
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
num_period = ''
with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('1M'):
        num_period = '1mo'
with col3:
    if st.button('6M'):
        num_period = '6mo'
with col4:
    if st.button('1YTD'):
        num_period = 'ytd'
with col5:
    if st.button('1Y'):
        num_period = '1y'
with col6:
    if st.button('5Y'):
        num_period = '5y'
with col7:
    if st.button('MAX'):
        num_period = 'max'

# Chart options
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    chart_type = st.selectbox('Chart Type', ['Candle', 'Line'])
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('Indicators', ['RSI', 'MACD'])
    else:
        indicators = st.selectbox('Indicators', ['RSI', 'Moving Average', 'MACD'])

# Get full history for charting
stock_data = yf.Ticker(ticker_input)
new_df1 = stock_data.history(period='max')
data1 = stock_data.history(period='max')

if num_period == '':
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)
    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)
    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average_forecast(data1), use_container_width=True)
    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
else:
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)
    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)
    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)
    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average_forecast(new_df1), use_container_width=True)
    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

# Volatility Analysis
st.subheader("Volatility Analysis")
window = st.slider("Rolling Window (days)", min_value=10, max_value=180, value=30)
data['Volatility'] = data['Close'].rolling(window=window).std()
fig_volatility = go.Figure(data=go.Scatter(x=data.index, y=data['Volatility'], mode='lines', name='Volatility'))
fig_volatility.update_layout(title="Stock Volatility", xaxis_title="Date", yaxis_title="Volatility")
st.plotly_chart(fig_volatility, use_container_width=True)

# Historical Returns Analysis
st.subheader("Historical Returns")
data['Daily Return'] = data['Close'].pct_change()
fig_returns = go.Figure(data=go.Scatter(x=data.index, y=data['Daily Return'], mode='lines', name='Daily Return'))
fig_returns.update_layout(title="Stock Daily Returns", xaxis_title="Date", yaxis_title="Daily Return")
st.plotly_chart(fig_returns, use_container_width=True)

returns_period = st.selectbox("Select Returns Period", ['1D', '1W', '1M', '3M', '1Y'])
if returns_period == '1D':
    st.write(f"**1-Day Return**: {data['Daily Return'].iloc[-1] * 100:.2f}%")
elif returns_period == '1W':
    if len(data) >= 5:
        weekly_return = ((data['Close'].iloc[-1] / data['Close'].iloc[-5]) - 1) * 100
        st.write(f"**1-Week Return**: {weekly_return.item():.2f}%")
    else:
        st.write("Not enough data for 1-week return.")
elif returns_period == '1M':
    if len(data) >= 21:
        monthly_return = ((data['Close'].iloc[-1] / data['Close'].iloc[-21]) - 1) * 100
        st.write(f"**1-Month Return**: {monthly_return.item():.2f}%")
    else:
        st.write("Not enough data for 1-month return.")
elif returns_period == '3M':
    if len(data) >= 63:
        three_month_return = ((data['Close'].iloc[-1] / data['Close'].iloc[-63]) - 1) * 100
        st.write(f"**3-Month Return**: {three_month_return.item():.2f}%")
    else:
        st.write("Not enough data for 3-month return.")
elif returns_period == '1Y':
    if len(data) >= 252:
        yearly_return = ((data['Close'].iloc[-1] / data['Close'].iloc[-252]) - 1) * 100
        st.write(f"**1-Year Return**: {yearly_return.item():.2f}%")
    else:
        st.write("Not enough data for 1-year return.")

# Download button for CSV export
csv_data = data.to_csv(index=True)
st.download_button(
    label="Download Stock Data as CSV",
    data=csv_data,
    file_name=f"{ticker_input}_stock_data.csv",
    mime="text/csv",
)
