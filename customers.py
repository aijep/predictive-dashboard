import streamlit as st
import pandas as pd

def show_customers():
    st.title("👥 Customer Management")
    st.write("View and manage customer details")

    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Contact": ["+91-9876543210", "+91-9123456780", "+91-9988776655"],
        "Bookings": [2, 1, 3]
    }
    df = pd.DataFrame(data)

    st.dataframe(df)

    st.text_input("Add New Customer Name")
    st.text_input("Add Contact Number")
    st.button("➕ Add Customer")
