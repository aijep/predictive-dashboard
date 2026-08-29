import streamlit as st
import pandas as pd
import sqlite3

def show_bookings():
    st.title("📅 Bookings Dashboard")

    conn = sqlite3.connect("business_dashboard.db")
    df = pd.read_sql_query("""
        SELECT b.id, c.name AS customer, b.type, b.status, b.created_at
        FROM bookings b
        LEFT JOIN customers c ON b.customer_id = c.id
    """, conn)
    st.dataframe(df)

    # Add new booking
    st.subheader("➕ Add Booking")
    customer_id = st.number_input("Customer ID", min_value=1)
    booking_type = st.selectbox("Booking Type", ["Training", "Farm Visit", "Product Order"])
    status = st.selectbox("Status", ["Pending", "Confirmed", "Cancelled"])

    if st.button("Save Booking"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (customer_id, type, status) VALUES (?, ?, ?)",
                       (customer_id, booking_type, status))
        conn.commit()
        st.success("✅ Booking added")
    conn.close()
