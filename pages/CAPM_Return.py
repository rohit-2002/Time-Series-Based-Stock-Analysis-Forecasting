import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import numpy as np
import plotly.express as px
import capm_functions

st.set_page_config(page_title="CAPM", 
                   page_icon="📈", 
                   layout="wide")

st.title("Capital Asset Pricing Model")

# Sidebar Information
st.sidebar.header("About the CAPM Calculator")
st.sidebar.write("""
    This tool allows you to calculate key metrics based on the Capital Asset Pricing Model (CAPM), including:
    
    - **Beta**: A measure of a stock's volatility relative to the market.
    - **Alpha**: The excess return on a stock relative to the expected return based on its beta.
    - **Expected Return**: Using the CAPM formula, we calculate the expected return for a stock given its beta and the market's return.
    - **Sharpe Ratio**: A ratio to evaluate the risk-adjusted return of a stock.
    - **Stock Volatility**: Measure of how much a stock's price fluctuates over time.
    - **Correlation Matrix**: Analyzing the relationship between stock returns and the market index.

    CAPM is a widely-used financial model that helps investors assess the expected return of an asset in relation to its risk, based on its beta value and the market's return.
    
    **Instructions**:
    1. Enter stock tickers separated by commas (e.g., 'TSLA, AAPL, AMZN').
    2. Choose the number of years of historical data for analysis.
    3. Set a risk-free rate (default is 5%).
    4. The app will display various metrics, including Beta, Alpha, Expected Return, Sharpe Ratio, and other financial insights.
""")

# st.markdown("""
# ### What We Provide in this Website:
# - **Stock Data Analysis**: Fetch and display stock closing prices for given tickers.
# - **Beta Calculation**: Understand how a stock moves in relation to the overall market.
# - **Expected Return Calculation**: Compute expected returns based on CAPM.
# - **Sharpe Ratio Analysis**: Evaluate the return per unit of risk.
# - **Correlation Matrix**: Identify relationships between stocks and the market.
# - **Stock Volatility Visualization**: See how volatile a stock is compared to others.
# - **Interactive Graphs & Data Download**: Visualize stock trends and download data for deeper analysis.
# """)

# Getting input from user
col1, col2 = st.columns([1, 1])
with col1:
    stock_input = st.text_input("Enter Stock Tickers (comma-separated)", 'TSLA,AAPL,AMZN,GOOGL')
    stock_list = [stock.strip().upper() for stock in stock_input.split(',')]
with col2:
    year = st.number_input("Number of years", 1, 10, value=1)
    rf_input = st.number_input("Risk-free Rate (%)", 0.0, 10.0, value=5.0) / 100  # User-defined risk-free rate

try:
    # Downloading data for S&P 500
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)
    SP500 = yf.download('^GSPC', start=start, end=end)['Close'].reset_index()
    SP500.columns = ['Date', 'SP500']

    stocks_df = pd.DataFrame()

    for stock in stock_list:
        data = yf.download(stock, start=start, end=end)
        stocks_df[stock] = data['Close']

    stocks_df.reset_index(inplace=True)
    stocks_df.loc[:, 'Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # Display dataframe for analysis
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### DataFrame Head')
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown('### DataFrame Tail')
        st.dataframe(stocks_df.tail(), use_container_width=True)

    # Visualizations
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown('### Price of all the Stocks')
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))
    with col2:
        st.markdown('### Normalized Stock Prices')
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

    stock_daily_return = capm_functions.daily_return(stocks_df)
    
    # Calculate beta and alpha
    beta = {}
    alpha = {}

    for i in stock_daily_return.columns:
        if i != 'Date' and i != 'SP500':
            b, a = capm_functions.calculate_beta(stock_daily_return, i)
            beta[i] = b
            alpha[i] = a

    beta_df = pd.DataFrame({'Stock': beta.keys(), 'Beta Value': [round(i, 2) for i in beta.values()]})

    # Display beta values
    with col1:
        st.markdown('### Calculated Beta Value')
        st.dataframe(beta_df, use_container_width=True) 

    # Market return
    rm = stock_daily_return['SP500'].mean() * 252  # Market return (annualized)
    
    # Calculate expected returns using CAPM
    return_df = pd.DataFrame()
    return_df['Stock'] = stock_list
    return_df['Return Value'] = [round(rf_input + (beta[stock] * (rm - rf_input)), 2) for stock in stock_list]

    # Display calculated returns
    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df, use_container_width=True)

    # Sharpe Ratio Calculation
    sharpe_ratios = {}
    for stock in stock_list:
        stock_volatility = stock_daily_return[stock].std() * np.sqrt(252)  # Annualized volatility
        sharpe_ratios[stock] = (return_df.loc[return_df['Stock'] == stock, 'Return Value'].values[0] - rf_input) / stock_volatility
    
    sharpe_ratio_df = pd.DataFrame({'Stock': sharpe_ratios.keys(), 'Sharpe Ratio': [round(i, 2) for i in sharpe_ratios.values()]})
    st.markdown('### Sharpe Ratio')
    st.dataframe(sharpe_ratio_df, use_container_width=True)

    # Correlation matrix
    corr_matrix = stock_daily_return.corr()
    st.markdown('### Correlation Matrix between Stock Returns and S&P 500')
    st.dataframe(corr_matrix, use_container_width=True)

    # Volatility Plot (Stock vs Market)
    volatility_df = pd.DataFrame({
        'Stock': stock_list,
        'Volatility': [stock_daily_return[stock].std() * np.sqrt(252) for stock in stock_list]
    })
    st.markdown('### Volatility of Stocks')
    st.bar_chart(volatility_df.set_index('Stock')['Volatility'])

    # Download data as CSV
    st.download_button("Download Data", stocks_df.to_csv(index=False), "stocks_data.csv", "text/csv")

except Exception as e:
    st.write(f'Error: {e}')
