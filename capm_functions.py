import plotly.express as px 
import numpy as np

# Function to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    fig.update_layout(width=450, margin=dict(l=20, r=20, t=50, b=20), 
                      legend=dict(orientation='h', yanchor='bottom', y=1.02, 
                                  xanchor='right', x=1))
    return fig

# Function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df.loc[:, i] = df[i] / df[i].iloc[0]  # Use .loc[] to avoid chained assignment
    return df

# Function to calculate daily returns
def daily_return(df):
    d_daily_return = df.copy()
    for i in df.columns[1:]:
        for j in range(1, len(df)):
            d_daily_return.loc[j, i] = ((df.loc[j, i] - df.loc[j - 1, i]) / df.loc[j - 1, i]) * 100
        d_daily_return.loc[0, i] = 0  # Set first value to 0 for daily return
    return d_daily_return

# Function to calculate beta
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['SP500'].mean() * 252  # Annualized market return
    b, a = np.polyfit(stocks_daily_return['SP500'], stocks_daily_return[stock], 1)
    return b, a
