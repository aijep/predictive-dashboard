import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def show_sales():
    st.title("📈 Sales Forecasting")
    st.write("Upload sales data and view forecasts")

    uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        dates = pd.date_range(start="2024-01-01", periods=100)
        df = pd.DataFrame({
            "date": dates,
            "sales": np.random.randint(50, 200, size=len(dates))
        })

    # Simple forecast
    df["day_num"] = np.arange(len(df))
    X = df[["day_num"]]
    y = df["sales"]
    model = LinearRegression().fit(X, y)
    future_days = np.arange(len(df), len(df) + 7).reshape(-1, 1)
    predictions = model.predict(future_days)

    future_df = pd.DataFrame({
        "date": pd.date_range(start=df["date"].iloc[-1] + pd.Timedelta(days=1), periods=7),
        "predicted_sales": predictions.astype(int)
    })

    fig, ax = plt.subplots()
    ax.plot(df["date"], df["sales"], label="Historical")
    ax.plot(future_df["date"], future_df["predicted_sales"], linestyle="--", label="Forecast")
    ax.legend()
    st.pyplot(fig)

    st.dataframe(future_df)
