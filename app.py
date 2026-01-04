import streamlit as st
from auth import signup, login
from db import create_tables

st.set_page_config(page_title="Smart Travel Planner", page_icon="✈️", layout="wide")

create_tables()

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.title("🔐 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login ✅"):
            user = login(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in Successfully ✅")
                st.rerun()
            else:
                st.error("Invalid Email or Password ❌")

    else:
        st.title("📝 Create Account")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Signup 🚀"):
            if signup(name, email, password):
                st.success("Account created ✅ Now Login")
            else:
                st.error("Email already exists ❌")

else:
    st.sidebar.success(f"👤 Welcome {st.session_state.user[1]}")

    menu = ["🏠 Dashboard", "🧭 Plan Trip", "💰 Manage Expenses"]
    choice = st.sidebar.radio("Navigation", menu)

    if st.sidebar.button("Logout ❌"):
        st.session_state.user = None
        st.rerun()

    if choice == "🏠 Dashboard":
        st.switch_page("pages/3_Dashboard.py")
    elif choice == "🧭 Plan Trip":
        st.switch_page("pages/1_Plan_Trip.py")
    elif choice == "💰 Manage Expenses":
        st.switch_page("pages/2_Manage_Expenses.py")
