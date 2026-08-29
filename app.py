import streamlit as st
import sales
import inventory
import bookings
import customers
from database import init_db

# Initialize database tables
init_db()

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
