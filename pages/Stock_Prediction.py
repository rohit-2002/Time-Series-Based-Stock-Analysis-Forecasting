import streamlit as st
import pandas as pd
from pages.utils.model_train import (
    get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling
)
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast
import numpy as np
np.isnan(np.nan) # returns True
# Streamlit page configuration
st.set_page_config(
    page_title="Stock Prediction",
    page_icon="⏳",
    layout="wide",
)

st.title("Stock Prediction Dashboard")


# User Input Section
col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')
    rmse = None  # Changed from 0 to None for better error handling

st.subheader(f'Predicting Next 30 Days Close Price for: {ticker}')

# Fetch stock data
close_price = get_data(ticker)

if close_price is None or close_price.empty:
    st.error("Error: Could not retrieve stock data. Please check the ticker symbol.")
else:
    # Data processing and model evaluation
    rolling_price = get_rolling_mean(close_price)
    differencing_order = get_differencing_order(rolling_price)
    scaled_data, scaler = scaling(rolling_price)
    rmse = evaluate_model(scaled_data, differencing_order)

    st.write("**Model RMSE Score:**", rmse)

    # Forecasting
    forecast = get_forecast(scaled_data, differencing_order)
    forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

    st.write('##### Forecast Data (Next 30 Days)')

    # Display forecast data in a table
    fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
    fig_tail.update_layout(height=220)
    st.plotly_chart(fig_tail, use_container_width=True)

    # Combine historical and forecasted data
    forecast = pd.concat([rolling_price, forecast])
    st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)

    # Download Button for Forecast Data
    csv = forecast.to_csv(index=True)
    st.download_button("Download Forecast Data", csv, "forecast.csv", "text/csv")

# Information about the code
st.sidebar.subheader("About This App")
st.sidebar.markdown("This Streamlit app predicts stock prices for the next 30 days based on historical data.")
st.sidebar.markdown("It uses rolling mean, differencing order, and scaling for data preprocessing before training the model.")
st.sidebar.markdown("The model's RMSE score is displayed for evaluation, and forecasted results are visualized using interactive plots.")
st.sidebar.markdown("Additional features like downloading forecast data and customizing prediction periods are available in the sidebar.")
