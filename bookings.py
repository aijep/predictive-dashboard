import streamlit as st
import pandas as pd

def show_bookings():
    st.title("📅 Bookings Dashboard")
    st.write("Manage customer bookings")

    data = {
        "Customer": ["Alice", "Bob", "Charlie"],
        "Booking Type": ["Training", "Farm Visit", "Product Order"],
        "Status": ["Confirmed", "Pending", "Cancelled"]
    }
    df = pd.DataFrame(data)

    st.dataframe(df)

    st.download_button(
        label="📥 Download Bookings CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="bookings.csv",
        mime="text/csv"
    )
