# pages/2_Manage_Expenses.py
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Manage Expenses", page_icon="💸")

st.title("💸 Manage Trip Expenses")

# ---- Ensure trip exists ----
trip = st.session_state.get("trip", None)
if trip is None:
    st.warning("No trip found. Please create a trip from the **Plan Trip** page first.")
    st.stop()

# ---- Initialize expenses in session_state ----
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

st.subheader(f"Destination: {trip.get('destination', 'N/A')}")
st.write(
    f"**Dates:** {trip.get('start_date')} → {trip.get('end_date')} | "
    f"**Days:** {trip.get('days')} | **Travelers:** {trip.get('travelers')}"
)


# ---- Expense Input Form ----
st.markdown("### ➕ Add a New Expense")

with st.form("expense_form", clear_on_submit=True):
    category = st.selectbox(
        "Category",
        ["Hotel", "Food", "Activities", "Transport", "Others"]
    )
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
    note = st.text_input("Note (optional)", "")
    exp_date = st.date_input("Date", value=date.today())

    submitted = st.form_submit_button("Add Expense")

if submitted:
    if amount <= 0:
        st.error("Amount should be greater than 0.")
    else:
        new_expense = {
            "Category": category,
            "Amount": float(amount),
            "Note": note,
            "Date": exp_date
        }
        st.session_state["expenses"].append(new_expense)
        st.success("Expense added successfully!")
        st.rerun()

# ---- Show Existing Expenses ----
expenses_data = st.session_state.get("expenses", [])

if not expenses_data:
    st.info("No expenses recorded yet.")
else:
    df_expenses = pd.DataFrame(expenses_data)
    st.markdown("### 📄 Recorded Expenses")
    st.dataframe(df_expenses, use_container_width=True)

    total_spent = df_expenses["Amount"].sum()
    st.metric("Total Actual Spent", f"₹{total_spent:,.0f}")

    # ---- Clear / Reset Expenses ----
    if st.button("🧹 Clear All Expenses"):
        st.session_state["expenses"] = []
        st.success("All expenses cleared.")
        st.rerun()
