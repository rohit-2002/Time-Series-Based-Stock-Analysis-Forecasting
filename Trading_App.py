# import streamlit as st 

# st.set_page_config(
#     page_title="Trading App",
#     page_icon="📉",
#     layout="wide"
# )

# st.title("Trading Guide App 📊")
# st.header("We provide the greatest platform for you to collect all information prior to investing in stocks.")
# st.image("app.png", use_container_width=True)

# st.markdown("## We provide the following services:")

# st.markdown("### :one: Stock Information")
# st.write("Through this page, you can see all the information about stocks.")

# st.markdown("### :two: Stock Prediction")
# st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models. Use this tool to gain valuable insights into market trends and make informed investment decisions.")

# st.markdown("### :three: CAPM Return")
# st.write("Discover the Capital Asset Pricing Model (CAPM), which calculates the expected return of different stock assets based on their risk and market performance.")

# st.markdown("### :four: CAPM Beta")
# st.write("Calculates Beta and expected return for individual stocks.")
import streamlit as st 

# Page configuration for a professional layout
st.set_page_config(
    page_title="Trading App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar with additional information or navigation
st.sidebar.header("Quick Navigation")
st.sidebar.write("Use the following options to explore the app:")
st.sidebar.markdown("""
- **Stock Information**: Get real-time stock data and historical performance.
- **Stock Prediction**: View predictions for stock prices.
- **CAPM Return**: Calculate expected returns using CAPM.
- **CAPM Beta**: Analyze stock risk and expected returns.
""")

# Main title with a modern gradient effect and subtitle
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>Trading Guide App 📊</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #666;'>Your ultimate platform for smarter stock investments</h3>", unsafe_allow_html=True)

# Display image with a subtle caption
st.image("app.png", use_container_width=True, caption="Explore the world of trading with us!")

# Services section with a stylish header
st.markdown("<h2 style='color: #ff7f0e; border-block-end: 2px solid #ff7f0e; padding-block-end: 5px;'>Our Premium Services</h2>", unsafe_allow_html=True)

# Service 1: Stock Information
st.markdown("<h3 style='color: #2ca02c;'>1. Stock Information</h3>", unsafe_allow_html=True)
st.write("Dive into comprehensive details about your favorite stocks. Get real-time data, historical performance, and key metrics—all in one place.")

# Service 2: Stock Prediction
st.markdown("<h3 style='color: #d62728;'>2. Stock Prediction</h3>", unsafe_allow_html=True)
st.write("Unlock the future with our cutting-edge forecasting tool! Explore predicted closing prices for the next 30 days, powered by historical data and advanced machine learning models. Stay ahead of market trends and invest with confidence.")

# Service 3: CAPM Return
st.markdown("<h3 style='color: #9467bd;'>3. CAPM Return</h3>", unsafe_allow_html=True)
st.write("Master your investments with the Capital Asset Pricing Model (CAPM). Calculate expected returns based on risk and market performance, helping you optimize your portfolio like a pro.")

# Service 4: CAPM Beta
st.markdown("<h3 style='color: #8c564b;'>4. CAPM Beta</h3>", unsafe_allow_html=True)
st.write("Measure the pulse of your stocks with Beta analysis. Understand risk levels and expected returns for individual assets, tailored to your investment strategy.")

# Footer for a polished finish
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Built with ❤️ by the Trading App Team | © 2025</p>", unsafe_allow_html=True)
