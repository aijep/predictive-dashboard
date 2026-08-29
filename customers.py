import streamlit as st
import pandas as pd
import sqlite3

def show_customers():
    st.title("👥 Customer Management")

    conn = sqlite3.connect("business_dashboard.db")
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    st.dataframe(df)

    # Add new customer
    st.subheader("➕ Add Customer")
    name = st.text_input("Name")
    contact = st.text_input("Contact")
    email = st.text_input("Email")
    location = st.text_input("Location")

    if st.button("Save Customer"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, contact, email, location) VALUES (?, ?, ?, ?)",
                       (name, contact, email, location))
        conn.commit()
        st.success(f"✅ Added {name}")
    conn.close()
