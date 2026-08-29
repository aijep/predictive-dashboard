import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load data
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

st.title("🧠 Predictive Sales Dashboard")
st.write("Explore forecasts by product and date range")

# Upload CSV
uploaded_file = st.file_uploader("Upload your sales data (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data uploaded successfully!")
else:
    st.info("Using sample data until a file is uploaded.")

# Filters
product_choice = st.selectbox("Select Product", df["product"].unique())
start_date, end_date = st.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

filtered_df = df[(df["product"] == product_choice) &
                 (df["date"] >= pd.to_datetime(start_date)) &
                 (df["date"] <= pd.to_datetime(end_date))]

# Train model
filtered_df["day_num"] = np.arange(len(filtered_df))
X = filtered_df[["day_num"]]
y = filtered_df["sales"]
model = LinearRegression().fit(X, y)

# Predict next 7 days
future_days = np.arange(len(filtered_df), len(filtered_df) + 7).reshape(-1, 1)
predictions = model.predict(future_days)
future_df = pd.DataFrame({
    "date": pd.date_range(start=filtered_df["date"].iloc[-1] + pd.Timedelta(days=1), periods=7),
    "predicted_sales": predictions.astype(int)
})

# Plot
fig, ax = plt.subplots()
ax.plot(filtered_df["date"], filtered_df["sales"], label="Historical Sales")
ax.plot(future_df["date"], future_df["predicted_sales"], label="Predicted Sales", linestyle="--")
ax.legend()
st.pyplot(fig)

st.write("Forecasted Sales")
st.dataframe(future_df)

# 🔹 Download button
csv = future_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name=f"{product_choice}_forecast.csv",
    mime="text/csv"
)
