from database import init_db
init_db()

import sqlite3
import streamlit_authenticator as stauth

# Connect to your existing database
conn = sqlite3.connect("business_dashboard.db")
cursor = conn.cursor()

# Hash the password securely (new API)
hashed_password = stauth.Hasher.hash("admin123")

# Insert a default admin user
cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin", hashed_password, "admin")
)

conn.commit()
conn.close()

print("✅ Admin user created: username=admin, password=admin123")
