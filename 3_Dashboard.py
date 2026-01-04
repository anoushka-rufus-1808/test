# pages/3_Dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Trip Dashboard")

# ---------- 1. Check trip in session_state ----------
trip = st.session_state.get("trip", None)

if trip is None:
    st.warning("No trip data found. Please plan a trip first from the **Plan Trip** page.")
    st.stop()

# Estimated total cost from Plan Trip
estimated_total = trip.get("estimate", 0)
breakdown = trip.get("breakdown", {})

st.subheader(f"Destination: {trip.get('destination', 'N/A')}")
st.write(f"**Days:** {trip.get('days', 'N/A')} | **Travelers:** {trip.get('travelers', 'N/A')}")

# ---------- 2. Load / get expenses (actual) ----------
expenses_data = st.session_state.get("expenses", None)

if expenses_data is None or len(expenses_data) == 0:
    st.info("No expenses recorded yet. Add expenses from the **Manage Expenses** page to see actual cost charts.")
    actual_total = 0
    df_expenses = pd.DataFrame(columns=["Category", "Amount"])
else:
    if isinstance(expenses_data, pd.DataFrame):
        df_expenses = expenses_data.copy()
    else:
        df_expenses = pd.DataFrame(expenses_data)

    if "Category" not in df_expenses.columns or "Amount" not in df_expenses.columns:
        st.error("Expenses data is missing required columns `Category` and `Amount`.")
        df_expenses = pd.DataFrame(columns=["Category", "Amount"])
        actual_total = 0
    else:
        actual_total = df_expenses["Amount"].sum()

# ---------- 3. Show key metrics ----------
col1, col2 = st.columns(2)
with col1:
    st.metric("Estimated Total Cost", f"₹{estimated_total:,.0f}")
with col2:
    st.metric("Actual Total Spent", f"₹{actual_total:,.0f}")

# ---------- 4. Estimated vs Actual – Bar Chart ----------
st.subheader("Estimated vs Actual Total Cost")

if estimated_total == 0 and actual_total == 0:
    st.info("No data available yet to compare estimated vs actual costs.")
else:
    labels = ["Estimated", "Actual"]
    values = [estimated_total, actual_total]

    fig_bar, ax_bar = plt.subplots()
    ax_bar.bar(labels, values)
    ax_bar.set_ylabel("Amount (₹)")
    ax_bar.set_title("Estimated vs Actual Total Cost")
    st.pyplot(fig_bar)

# ---------- 5. Pie Chart – Actual Expense Breakdown ----------
st.subheader("Actual Expenses by Category")

if df_expenses.empty:
    st.info("No actual expenses recorded yet to show category-wise breakdown.")
else:
    cat_group = df_expenses.groupby("Category")["Amount"].sum()

    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(cat_group.values, labels=cat_group.index, autopct="%1.1f%%")
    ax_pie.set_title("Actual Expense Breakdown by Category")
    st.pyplot(fig_pie)

# ---------- 6. Optional: show table of expenses ----------
if not df_expenses.empty:
    st.subheader("📄 Expense Details")
    st.dataframe(df_expenses, use_container_width=True)
