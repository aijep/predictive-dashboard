import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import pandas as pd

# --- DATABASE CONNECTION ---
conn = sqlite3.connect("business_dashboard.db")
cursor = conn.cursor()

# --- LOAD USERS FROM DATABASE ---
cursor.execute("SELECT username, password, role FROM users")
rows = cursor.fetchall()

credentials = {
    "usernames": {
        row[0]: {
            "name": row[0].capitalize(),
            "password": row[1],
            "role": row[2]
        }
        for row in rows
    }
}

# --- AUTHENTICATION SETUP ---
authenticator = stauth.Authenticate(
    credentials,
    "dashboard_cookie",
    "random_key",
    cookie_expiry_days=30
)

# --- LOGIN FORM ---
name, authentication_status, username = authenticator.login("Login", "main")  # ✅ valid location

# --- LOGIN LOGIC ---
if authentication_status:
    st.sidebar.success(f"Welcome, {name}!")
    role = credentials["usernames"][username]["role"]

    # --- ROLE‑BASED DASHBOARD ---
    if role == "admin":
        st.title("Admin Dashboard")
        st.write("Manage products, bookings, and users here.")
        df = pd.read_sql_query("SELECT * FROM users", conn)
        st.dataframe(df)

    elif role == "manager":
        st.title("Manager Dashboard")
        st.write("View bookings and inventory.")
        df = pd.read_sql_query("SELECT * FROM bookings", conn)
        st.dataframe(df)

    else:
        st.title("User Dashboard")
        st.write("Welcome to the business dashboard!")

    authenticator.logout("Logout", "sidebar")

elif authentication_status is False:
    st.error("Username or password is incorrect.")
else:
    st.warning("Please enter your credentials.")
