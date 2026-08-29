import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load sample data
@st.cache_data
def load_data():
    dates = pd.date_range(start="2024-01-01", periods=100)
    products = ["Bread", "Cake", "Cookies"]
    data = {
        "date": np.tile(dates, len(products)),
        "product": np.repeat(products, len(dates)),
        "sales": np.random.randint(50, 200, size=len(dates) * len(products))
    }
    return pd.DataFrame(data)

df = load_data()

# App title
st.title("🧠 Predictive Sales Dashboard")
st.write("Explore forecasts by product and date range")

# Upload CSV
uploaded_file = st.file_uploader("Upload your sales data (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data uploaded successfully!")
else:
    st.info("Using sample data until a file is uploaded.")

# Product filter with “All Products” option
product_options = ["All Products"] + list(df["product"].unique())
product_choice = st.selectbox("Select Product", product_options)

# Date range filter
start_date, end_date = st.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

# Filter data
filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) &
                 (df["date"] <= pd.to_datetime(end_date))]

# Forecast function
def forecast_product(data, product_name):
    data = data[data["product"] == product_name].copy()
    data["day_num"] = np.arange(len(data))
    X = data[["day_num"]]
    y = data["sales"]
    model = LinearRegression().fit(X, y)
    future_days = np.arange(len(data), len(data) + 7).reshape(-1, 1)
    predictions = model.predict(future_days)
    return pd.DataFrame({
        "product": product_name,
        "date": pd.date_range(start=data["date"].iloc[-1] + pd.Timedelta(days=1), periods=7),
        "predicted_sales": predictions.astype(int)
    })

# Generate forecasts
if product_choice == "All Products":
    forecast_list = []
    for p in df["product"].unique():
        forecast_list.append(forecast_product(filtered_df, p))
    future_df = pd.concat(forecast_list, ignore_index=True)
else:
    future_df = forecast_product(filtered_df, product_choice)

# Plot
fig, ax = plt.subplots()
if product_choice == "All Products":
    for p in df["product"].unique():
        subset = filtered_df[filtered_df["product"] == p]
        ax.plot(subset["date"], subset["sales"], label=f"{p} Historical")
        subset_future = future_df[future_df["product"] == p]
        ax.plot(subset_future["date"], subset_future["predicted_sales"], linestyle="--", label=f"{p} Forecast")
else:
    ax.plot(filtered_df["date"], filtered_df["sales"], label="Historical Sales")
    ax.plot(future_df["date"], future_df["predicted_sales"], linestyle="--", label="Predicted Sales")

ax.legend()
st.pyplot(fig)

# Display forecast
st.write("Forecasted Sales")
st.dataframe(future_df)

# Download button
csv = future_df.to_csv(index=False).encode('utf-8')
file_name = "All_Products_forecast.csv" if product_choice == "All Products" else f"{product_choice}_forecast.csv"
st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name=file_name,
    mime="text/csv"
)
