import streamlit as st
import pandas as pd
import sqlite3

def show_inventory():
    st.title("📦 Inventory Management")

    conn = sqlite3.connect("business_dashboard.db")
    df = pd.read_sql_query("SELECT * FROM inventory", conn)

    st.dataframe(df)

    # Add new product
    st.subheader("➕ Add Product")
    product = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    reorder = st.number_input("Reorder Point", min_value=0)

    if st.button("Save Product"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (product_name, price, stock, reorder_point) VALUES (?, ?, ?, ?)",
                       (product, price, stock, reorder))
        conn.commit()
        st.success(f"✅ Added {product}")
    conn.close()
