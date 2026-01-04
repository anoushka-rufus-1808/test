# pages/1_Plan_Trip.py

import streamlit as st
import pandas as pd
import math
import requests
from datetime import date, timedelta

st.set_page_config(page_title="Plan Trip", page_icon="🧭")

st.title("🧭 Smart Trip Planner")
st.caption("Plan smarter trips with cost estimates, dates, and personalization")

# ---- Load Dataset ----
@st.cache_data
def load_tour_data():
    return pd.read_csv("india_tour_data.csv")

try:
    df = load_tour_data()
except FileNotFoundError:
    st.error("❌ Could not find `india_tour_data.csv`.")
    st.stop()

# ---- Weather API ----
def get_weather(city):
    try:
        API_KEY = "31b5f3e64639d63a06288a47ef6b9783"
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return data["main"]["temp"], data["weather"][0]["description"]
    except:
        pass
    return None, None

# ---- User Inputs ----
destination = st.selectbox("📍 Select Destination", df["Destination"].unique())

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=date.today())
with col2:
    end_date = st.date_input("End Date", value=date.today() + timedelta(days=2))

# auto-calc days
days = max((end_date - start_date).days, 1)

travelers = st.number_input("Number of Travelers", min_value=1, max_value=20, value=2)

occupancy = st.slider(
    "People per Room",
    min_value=1,
    max_value=4,
    value=2
)

budget = st.number_input(
    "Your Budget (₹)",
    min_value=1000,
    max_value=500000,
    value=20000
)

travel_style = st.selectbox(
    "Travel Style",
    ["Relaxed", "Adventure", "Budget", "Luxury"]
)

pace = st.slider(
    "Trip Pace",
    min_value=1,
    max_value=5,
    value=3,
    help="1 = relaxed, 5 = packed"
)

# ---- Destination Row ----
place = df[df["Destination"] == destination].iloc[0]

# ---- Weather Info + Tips ----
temp, desc = get_weather(destination)
if temp:
    st.info(f"🌤 Weather in {destination}: {temp}°C, {desc.capitalize()}")

    # Weather-based suggestion
    if "rain" in desc.lower():
        st.warning("🌧 Rain expected. Indoor attractions and buffer time recommended.")
    elif temp >= 35:
        st.warning("🔥 High temperature. Plan outdoor activities early morning or evening.")

# ---- Generate Plan ----
if st.button("✨ Generate Plan"):
    rooms = math.ceil(travelers / occupancy)

    hotel_cost = place["HotelCost"] * days * rooms
    food_cost = place["FoodCost"] * days * travelers
    activity_cost = place["ActivitiesCost"] * days * travelers
    transport_cost = place["TransportCost"]

    total_estimated = hotel_cost + food_cost + activity_cost + transport_cost

    # ---- Pace-based message ----
    if pace >= 4:
        st.warning("⚠ Packed itinerary selected. Expect higher fatigue and tighter schedules.")
    elif pace <= 2:
        st.info("😌 Relaxed pace selected. Ideal for leisure-focused travel.")

    # ---- Trip Summary ----
    st.subheader("🧾 Trip Summary")
    st.markdown(f"""
    - **Destination:** {destination}  
    - **Dates:** {start_date} → {end_date}  
    - **Duration:** {days} days  
    - **Travelers:** {travelers}  
    - **Travel Style:** {travel_style}  
    - **Trip Pace:** {pace}/5  
    - **Rooms Required:** {rooms}
    """)

    # ---- Sample Itinerary ----
    st.subheader("🗓 Sample Itinerary")
    for i in range(days):
        current_day = start_date + timedelta(days=i)
        st.markdown(f"""
        **Day {i+1} ({current_day})**
        - Morning: Local sightseeing & breakfast
        - Afternoon: Popular attractions & lunch
        - Evening: Leisure activities / shopping
        """)

    # ---- Cost Breakdown ----
    st.subheader("📊 Estimated Cost Breakdown")
    breakdown = {
        "Hotel": f"₹{hotel_cost:,}",
        "Food": f"₹{food_cost:,}",
        "Activities": f"₹{activity_cost:,}",
        "Transport": f"₹{transport_cost:,}"
    }
    st.table(pd.DataFrame(breakdown.items(), columns=["Category", "Cost (₹)"]))

    st.metric("💰 Total Estimated Cost", f"₹{total_estimated:,}")

    # ---- Save to session_state ----
    st.session_state["trip"] = {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "travelers": travelers,
        "rooms": rooms,
        "estimate": total_estimated,
        "budget": budget,
        "pace": pace,
        "style": travel_style
    }

    st.session_state["expenses"] = []

    # ---- Budget Feedback ----
    if total_estimated > budget:
        st.error(f"⚠ Over Budget by ₹{total_estimated - budget:,}")
    else:
        st.success(f"✅ Within Budget! You save ₹{budget - total_estimated:,}")

    st.info("Proceed to **Manage Expenses** to track actual spending.")
