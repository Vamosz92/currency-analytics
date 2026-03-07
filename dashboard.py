import streamlit as st
import json

with open("analytics.json") as f:
    analytics = json.load(f)

st.title("EUR → HUF Exchange rate analytics")

st.subheader("Main analytics")
st.metric("Total return %", analytics["total_return_pct"])
st.metric("Daily volatility", analytics["daily_volatility"])
st.metric("Maximum drawdown", analytics["max_drawdown"])

st.subheader("Moving averages")
st.write(f"30-day: {analytics['moving_avg_30']}")
st.write(f"60-day: {analytics['moving_avg_60']}")
st.write(f"90-day: {analytics['moving_avg_90']}")

st.subheader("Trend")
st.write(f"Slope: {analytics['trend_slope']}")