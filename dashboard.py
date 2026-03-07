import streamlit as st
import json

with open("analytics.json") as f:
    analytics = json.load(f)

st.title("EUR → HUF Exchange Rate Analytics")
st.markdown("Dashboard showing exchange rate performance and key financial indicators.")

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Return %", f"{analytics['total_return_pct']:.2f}%")
col2.metric("Daily Volatility", f"{analytics['daily_volatility']:.4f}")
col3.metric("Maximum Drawdown", f"{analytics['max_drawdown']:.2f}%")

st.subheader("Moving averages")
st.write(f"30-day: {analytics['moving_avg_30']}")
st.write(f"60-day: {analytics['moving_avg_60']}")
st.write(f"90-day: {analytics['moving_avg_90']}")

st.subheader("Trend")
st.write(f"Slope: {analytics['trend_slope']:.4f}")
