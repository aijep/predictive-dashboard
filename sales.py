import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sqlite3

def show_sales():
    st.title("📈 Sales Forecasting")

    # Load sales data from bookings + inventory linkage
    conn = sqlite3.connect("business_dashboard.db")
    df = pd.read_sql_query("""
        SELECT b.id, b.type, b.created_at, c.name AS customer, i.product_name, i.price
        FROM bookings b
        LEFT JOIN customers c ON b.customer_id = c.id
        LEFT JOIN inventory i ON b.id = i.id
    """, conn)
    conn.close()

    if df.empty:
        st.info("No sales data yet. Add bookings and inventory first.")
        return

    # Forecast example (using booking dates)
    df["date"] = pd.to_datetime(df["created_at"])
    df["day_num"] = np.arange(len(df))
    X = df[["day_num"]]
    y = np.random.randint(50, 200, size=len(df))  # placeholder sales values
    model = LinearRegression().fit(X, y)

    future_days = np.arange(len(df), len(df) + 7).reshape(-1, 1)
    predictions = model.predict(future_days)

    future_df = pd.DataFrame({
        "date": pd.date_range(start=df["date"].iloc[-1] + pd.Timedelta(days=1), periods=7),
        "predicted_sales": predictions.astype(int)
    })

    fig, ax = plt.subplots()
    ax.plot(df["date"], y, label="Historical")
    ax.plot(future_df["date"], future_df["predicted_sales"], linestyle="--", label="Forecast")
    ax.legend()
    st.pyplot(fig)

    st.dataframe(future_df)
