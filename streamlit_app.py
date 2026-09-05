
from pathlib import Path
import pandas as pd
import streamlit as st

BASE = Path(__file__).parent

pred = pd.read_csv(
    BASE / "final_test_predictions_with_intervals.csv",
    parse_dates=["Date"]
)

summary = pd.read_csv(
    BASE / "final_model_summary.csv"
)

selected_model = summary.loc[0, "Selected_Model"]

available = pred[
    pred["model_A01"].notna() &
    pred[selected_model].notna() &
    pred["Lower_90"].notna() &
    pred["Upper_90"].notna()
].copy()

available = available.sort_values("Date").reset_index(drop=True)

st.set_page_config(
    page_title="NHS 111 England Forecast",
    layout="centered"
)

st.title("NHS 111 Daily Call Demand Forecast — England")

st.write(
    "This tool shows one-day-ahead forecasts for the total number "
    "of NHS 111 calls across England during the held-out evaluation period."
)

if available.empty:
    st.error("No complete held-out forecast dates are available.")
    st.stop()

valid_dates = available["Date"].dt.strftime("%d %B %Y").tolist()

st.info(
    f"Available evaluation dates: "
    f"{available['Date'].min().strftime('%d %B %Y')} to "
    f"{available['Date'].max().strftime('%d %B %Y')}. "
    "Known partial-reporting targets are excluded."
)

selected_text = st.selectbox(
    "Select a forecast date",
    valid_dates
)

selected_date = pd.to_datetime(
    selected_text,
    format="%d %B %Y"
)

row = available[
    available["Date"] == selected_date
].iloc[0]

predicted = float(row[selected_model])
actual = float(row["model_A01"])
lower = float(row["Lower_90"])
upper = float(row["Upper_90"])
absolute_error = abs(actual - predicted)

st.subheader("Forecast result")

col1, col2 = st.columns(2)

col1.metric(
    "Predicted calls",
    f"{predicted:,.0f}"
)

col2.metric(
    "Actual reported calls",
    f"{actual:,.0f}"
)

col3, col4 = st.columns(2)

col3.metric(
    "Absolute error",
    f"{absolute_error:,.0f} calls"
)

col4.metric(
    "90% prediction interval",
    f"{lower:,.0f} to {upper:,.0f}"
)

st.caption(
    "The interval uses the 90th percentile of absolute one-day-ahead "
    "errors from training-period walk-forward validation."
)

chart_start = selected_date - pd.Timedelta(days=28)

chart = available[
    (available["Date"] >= chart_start) &
    (available["Date"] <= selected_date)
][
    ["Date", "model_A01", selected_model]
].copy()

chart = chart.set_index("Date")

chart.columns = [
    "Actual calls",
    "Predicted calls"
]

st.subheader("Recent actual and predicted demand")

st.line_chart(chart)

st.caption(
    f"Forecasting area: England. Model used: {selected_model}. "
    "The selectable dates are held-out evaluation dates."
)
