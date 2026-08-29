import streamlit as st
import pandas as pd

def show_inventory():
    st.title("📦 Inventory Management")
    st.write("Track stock levels and reorder alerts")

    data = {
        "Product": ["Bread", "Cake", "Cookies"],
        "Stock": [20, 5, 12],
        "Reorder Point": [10, 10, 10]
    }
    df = pd.DataFrame(data)

    st.dataframe(df)

    low_stock = df[df["Stock"] < df["Reorder Point"]]
    if not low_stock.empty:
        st.warning("⚠️ Reorder needed for: " + ", ".join(low_stock["Product"]))
