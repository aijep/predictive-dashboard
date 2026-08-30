import streamlit as st
import streamlit_authenticator as stauth
import sqlite3

# --- Database connection ---
conn = sqlite3.connect("business_dashboard.db")
cursor = conn.cursor()

# --- Fetch users from database ---
cursor.execute("SELECT username, password, role FROM users")
rows = cursor.fetchall()
conn.close()

# --- Build credentials dictionary ---
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

# --- Authentication setup ---
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="dashboard_cookie",
    key="secret_key",
    cookie_expiry_days=30
)

# --- Login form ---
authenticator.login(location="main")

# --- Dashboard logic ---
if st.session_state.get("authentication_status"):
    name = st.session_state["name"]
    username = st.session_state["username"]

    st.sidebar.title(f"Welcome, {name} 👋")
    authenticator.logout("Logout", "sidebar")  # Added logout button

    st.title("Predictive Business Dashboard")
    st.success("✅ Streamlit is running correctly.")
    st.write("You are logged in as:", username)
    st.write("Role:", credentials["usernames"][username]["role"])
    st.write("This is your main dashboard area.")
    st.write("Add your modules here — sales, inventory, bookings, etc.")

elif st.session_state.get("authentication_status") is False:
    st.error("Username or password is incorrect.")
else:
    st.warning("Please log in to continue.")
