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

# Product filter
product_choice = st.selectbox("Select Product", df["product"].unique())

# Date range filter
start_date, end_date = st.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
