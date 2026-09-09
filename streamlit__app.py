
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

BASE = Path(__file__).parent

st.set_page_config(
    page_title="NHS 111 Call Forecast in England",
    page_icon="☎️",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background: #ffffff;
        color: #111827;
    }

    .block-container {
        max-width: 920px;
        padding-top: 4.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        font-family: Arial, sans-serif;
        color: #111827;
    }

    .main-title {
        font-size: 2.15rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.35rem;
        color: #111827;
    }

    .subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 1.8rem;
    }

    .forecast-card {
        background: #f8fbff;
        border: 1px solid #e4edf7;
        border-radius: 24px;
        padding: 28px;
        margin-top: 18px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }

    .date-label {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 6px;
    }

    .forecast-number {
        color: #0f172a;
        font-size: 3.2rem;
        font-weight: 750;
        line-height: 1.05;
        margin-top: 4px;
    }

    .forecast-label {
        color: #64748b;
        font-size: 1rem;
        margin-top: 5px;
    }

    .small-card {
        background: #ffffff;
        border: 1px solid #e7edf4;
        border-radius: 18px;
        padding: 18px;
        min-height: 118px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    .small-label {
        color: #64748b;
        font-size: 0.88rem;
        margin-bottom: 6px;
    }

    .small-value {
        color: #111827;
        font-size: 1.45rem;
        font-weight: 700;
    }

    .small-note {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 5px;
    }

    .chart-title {
        color: #111111;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 0.7rem;
    }

    div[data-baseweb="select"] > div {
        background: #ffffff;
        color: #111827;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

prediction_file = BASE / "final_test_predictions_with_intervals.csv"

if not prediction_file.exists():
    st.error("Forecast results could not be found. Run the notebook cells that create the final results first.")
    st.stop()

pred = pd.read_csv(prediction_file, parse_dates=["Date"])

required = ["Date", "model_A01", "Lower_90", "Upper_90"]
missing = [column for column in required if column not in pred.columns]

if missing:
    st.error("The forecast results file is incomplete. Run the final notebook cells again.")
    st.stop()

summary_file = BASE / "final_model_summary.csv"

if summary_file.exists():
    summary = pd.read_csv(summary_file)
    selected_model = str(summary.loc[0, "Selected_Model"])
else:
    selected_model = "Tuned CatBoost"

if selected_model not in pred.columns:
    st.error("The selected forecast model is not available in the results file.")
    st.stop()

available = pred[
    pred["model_A01"].notna() &
    pred[selected_model].notna() &
    pred["Lower_90"].notna() &
    pred["Upper_90"].notna()
].copy()

available = available.sort_values("Date").reset_index(drop=True)

if available.empty:
    st.error("No complete forecast dates are available.")
    st.stop()

st.markdown(
    '<div class="main-title">NHS 111 Daily Call Forecast in England</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Choose a date to see the predicted and reported number of NHS 111 calls.</div>',
    unsafe_allow_html=True
)

date_labels = available["Date"].dt.strftime("%A %d %B %Y").tolist()

selected_text = st.selectbox(
    "Choose a date",
    date_labels,
    index=len(date_labels) - 1
)

selected_date = pd.to_datetime(
    selected_text,
    format="%A %d %B %Y"
)

row = available.loc[
    available["Date"] == selected_date
].iloc[0]

predicted = float(row[selected_model])
actual = float(row["model_A01"])
lower = float(row["Lower_90"])
upper = float(row["Upper_90"])

absolute_error = abs(actual - predicted)
percentage_error = 100 * absolute_error / actual if actual else 0

st.markdown(
    f"""
    <div class="forecast-card">
        <div class="date-label">{selected_date.strftime("%A %d %B %Y")}</div>
        <div class="forecast-number">{predicted:,.0f}</div>
        <div class="forecast-label">predicted calls</div>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="small-card">
            <div class="small-label">Reported calls</div>
            <div class="small-value">{actual:,.0f}</div>
            <div class="small-note">Actual calls recorded</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="small-card">
            <div class="small-label">Forecast error</div>
            <div class="small-value">{absolute_error:,.0f}</div>
            <div class="small-note">{percentage_error:.1f}% of reported calls</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="small-card">
            <div class="small-label">Expected range</div>
            <div class="small-value">{lower:,.0f} to {upper:,.0f}</div>
            <div class="small-note">90% empirical forecast range</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="chart-title">Calls in this period</div>',
    unsafe_allow_html=True
)

chart_start = selected_date - pd.Timedelta(days=28)

chart = available[
    (available["Date"] >= chart_start) &
    (available["Date"] <= selected_date)
][["Date", "model_A01", selected_model]].copy()

chart = chart.rename(
    columns={
        "model_A01": "Reported calls",
        selected_model: "Predicted calls"
    }
)

chart_long = chart.melt(
    id_vars="Date",
    value_vars=["Reported calls", "Predicted calls"],
    var_name="Type",
    value_name="Calls"
)

calls_chart = (
    alt.Chart(chart_long)
    .mark_line(
        point=True,
        strokeWidth=2.5
    )
    .encode(
        x=alt.X(
            "Date:T",
            title=None,
            axis=alt.Axis(
                format="%d %b",
                labelColor="#111827",
                labelAngle=0,
                grid=False
            )
        ),
        y=alt.Y(
            "Calls:Q",
            title="Calls",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(
                labelColor="#111827",
                titleColor="#111827",
                gridColor="#d7e9f7"
            )
        ),
        color=alt.Color(
            "Type:N",
            title=None,
            scale=alt.Scale(
                domain=["Reported calls", "Predicted calls"],
                range=["#111111", "#4da8e8"]
            ),
            legend=alt.Legend(
                orient="top",
                labelColor="#111827"
            )
        ),
        tooltip=[
            alt.Tooltip(
                "Date:T",
                title="Date",
                format="%A %d %B %Y"
            ),
            alt.Tooltip(
                "Type:N",
                title="Type"
            ),
            alt.Tooltip(
                "Calls:Q",
                title="Calls",
                format=","
            )
        ]
    )
  .properties(
    height=300,
    background="#f4f9ff"
)
.configure_view(
    stroke=None,
    fill="#f4f9ff"
)
)

st.altair_chart(
    calls_chart,
    use_container_width=True
)

st.caption(
    "The expected range is calculated from earlier one day ahead forecast errors. "
    "It is an empirical range and does not guarantee that every future value will fall inside it."
)
