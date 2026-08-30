import streamlit as st
import sales
import inventory
import bookings
import customers
from database import init_db
import sqlite3
import streamlit_authenticator as stauth

# Initialize database
init_db()

# Fetch users from DB
def get_users():
    conn = sqlite3.connect("business_dashboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

users = get_users()
if not users:
    st.warning("⚠️ No users found. Please add at least one user in the database.")

# Prepare authenticator
names = [u[0] for u in users]
usernames = [u[0] for u in users]
passwords = [u[1] for u in users]  # already hashed in DB

authenticator = stauth.Authenticate(
    names, usernames, passwords,
    "dashboard_cookie", "secret_key", cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

# Authentication flow
if authentication_status:
    st.sidebar.success(f"Welcome {name} 👋")

    # Sidebar navigation
    st.sidebar.title("📊 Business Dashboard")
    option = st.sidebar.radio(
        "Choose a module",
        ["Sales", "Inventory", "Bookings", "Customers"]
    )

    # Route to modules
    if option == "Sales":
        sales.show_sales()
    elif option == "Inventory":
        inventory.show_inventory()
    elif option == "Bookings":
        bookings.show_bookings()
    elif option == "Customers":
        customers.show_customers()

    # Logout
    authenticator.logout("Logout", "sidebar")

    # Footer
    st.markdown("---")
    st.caption("🧠 Predictive Business Dashboard © 2026 | Powered by Streamlit + SQLite")

elif authentication_status is False:
    st.error("Invalid username or password")
elif authentication_status is None:
    st.warning("Please enter your credentials")
