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
st.write("Forecast sales by product with confidence intervals and summary metrics")

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

# Color palette per product
color_map = {
    "Bread": "brown",
    "Cake": "purple",
    "Cookies": "orange"
}

# Forecast function with confidence intervals
def forecast_product(data, product_name):
    data = data[data["product"] == product_name].copy()
    data["day_num"] = np.arange(len(data))
    X = data[["day_num"]]
    y = data["sales"]
    model = LinearRegression().fit(X, y)
    future_days = np.arange(len(data), len(data) + 7).reshape(-1, 1)
    predictions = model.predict(future_days)

    # Confidence intervals (± standard deviation of residuals)
    residuals = y - model.predict(X)
    std_dev = residuals.std()
    lower_bound = predictions - std_dev
    upper_bound = predictions + std_dev

    return pd.DataFrame({
        "product": product_name,
        "date": pd.date_range(start=data["date"].iloc[-1] + pd.Timedelta(days=1), periods=7),
        "predicted_sales": predictions.astype(int),
        "lower_ci": lower_bound.astype(int),
        "upper_ci": upper_bound.astype(int)
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
        ax.plot(subset["date"], subset["sales"], label=f"{p} Historical", color=color_map[p])
        subset_future = future_df[future_df["product"] == p]
        ax.plot(subset_future["date"], subset_future["predicted_sales"], linestyle="--", label=f"{p} Forecast", color=color_map[p])
        ax.fill_between(subset_future["date"], subset_future["lower_ci"], subset_future["upper_ci"], color=color_map[p], alpha=0.2)
else:
    ax.plot(filtered_df["date"], filtered_df["sales"], label="Historical Sales", color=color_map[product_choice])
    ax.plot(future_df["date"], future_df["predicted_sales"], linestyle="--", label="Predicted Sales", color=color_map[product_choice])
    ax.fill_between(future_df["date"], future_df["lower_ci"], future_df["upper_ci"], color=color_map[product_choice], alpha=0.2)

ax.legend()
st.pyplot(fig)

# Display forecast
st.write("Forecasted Sales with Confidence Intervals")
st.dataframe(future_df)

# Summary metrics
st.subheader("📊 Summary Metrics")
summary = future_df.groupby("product")["predicted_sales"].sum().reset_index()
summary.rename(columns={"predicted_sales": "Total Forecasted Sales"}, inplace=True)
st.table(summary)

# Download button
csv = future_df.to_csv(index=False).encode('utf-8')
file_name = "All_Products_forecast.csv" if product_choice == "All Products" else f"{product_choice}_forecast.csv"
st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name=file_name,
    mime="text/csv"
)
