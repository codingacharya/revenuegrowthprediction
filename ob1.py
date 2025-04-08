import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Revenue Growth Predictor", layout="centered")

st.title("📈 Startup Revenue Growth Trajectory Predictor")

st.markdown("This tool forecasts a startup's revenue over the next 1–5 years using financial and market indicators.")

st.sidebar.header("Enter Company Metrics")

# Input Features
initial_revenue = st.sidebar.number_input("Current Annual Revenue ($)", min_value=10000, value=500000, step=10000)
profit_margin = st.sidebar.slider("Profit Margin (%)", min_value=0, max_value=100, value=20)
funding_received = st.sidebar.number_input("Total Funding Received ($)", min_value=0, value=1000000, step=10000)
burn_rate = st.sidebar.number_input("Monthly Burn Rate ($)", min_value=0, value=50000, step=1000)
market_growth = st.sidebar.slider("Market Growth Rate (%)", min_value=0, max_value=100, value=10)
customer_acquisition_cost = st.sidebar.number_input("Customer Acquisition Cost (CAC) ($)", min_value=0, value=100)
customer_lifetime_value = st.sidebar.number_input("Customer Lifetime Value (LTV) ($)", min_value=0, value=1000)
social_sentiment = st.sidebar.slider("Social Media Sentiment (0-1)", min_value=0.0, max_value=1.0, value=0.6, step=0.01)

# Time period
forecast_years = st.slider("Forecast Years", min_value=1, max_value=5, value=3)

# Mock predictive logic using a basic model
def predict_revenue(initial, growth_rate, years):
    projected = []
    revenue = initial
    for year in range(1, years + 1):
        revenue *= (1 + growth_rate)
        projected.append((year, revenue))
    return projected

# Composite growth rate estimation (simple heuristic model)
base_growth_rate = market_growth / 100
modifier = (profit_margin / 100) + (social_sentiment * 0.2) + ((customer_lifetime_value - customer_acquisition_cost) / 10000)
burn_modifier = -burn_rate / 1000000

# Total growth rate estimate
estimated_growth_rate = base_growth_rate + modifier + burn_modifier

# Make predictions
forecast = predict_revenue(initial_revenue, estimated_growth_rate, forecast_years)
forecast_df = pd.DataFrame(forecast, columns=["Year", "Projected Revenue"])

# Plotting
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=forecast_df["Year"],
    y=forecast_df["Projected Revenue"],
    mode='lines+markers',
    name="Projected Revenue",
    line=dict(color='green')
))
fig.update_layout(title="📊 Projected Revenue Over Time",
                  xaxis_title="Years from Now",
                  yaxis_title="Revenue ($)",
                  template="plotly_white")

st.plotly_chart(fig)

# Display data
st.subheader("📄 Forecast Table")
st.dataframe(forecast_df.style.format({"Projected Revenue": "${:,.2f}"}))

# Show estimated growth rate
st.info(f"📌 Estimated Annual Growth Rate: **{(estimated_growth_rate * 100):.2f}%**")

# Note
st.markdown("---")
st.caption("🔍 This is a prototype tool. Replace the model logic with real ML predictions for production use.")
