# pages/1_Plan_Trip.py
st.cache_data.clear()
import streamlit as st
import pandas as pd
import math
import requests

st.set_page_config(page_title="Plan Trip", page_icon="🧭")

st.title("🧭 Smart Trip Planner")
st.caption("Plan smarter trips with cost estimates and personalization")

# ---- Load Dataset ----
@st.cache_data
def load_tour_data():
    return pd.read_csv("india_tour_data.csv")

try:
    df = load_tour_data()
except FileNotFoundError:
    st.error(
        "❌ Could not find `india_tour_data.csv`.\n\n"
        "Make sure the file is in the project root or update the path."
    )
    st.stop()

# ---- Weather API (safe + optional) ----
def get_weather(city):
    try:
        API_KEY = "31b5f3e64639d63a06288a47ef6b9783"  # put key here
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
    days = st.number_input("Days of Stay", min_value=1, max_value=30, value=2)
with col2:
    travelers = st.number_input("Number of Travelers", min_value=1, max_value=20, value=2)

occupancy = st.slider(
    "People per Room",
    min_value=1,
    max_value=4,
    value=2,
    help="Used to calculate number of hotel rooms"
)

budget = st.number_input(
    "Your Budget (₹)",
    min_value=1000,
    max_value=500000,
    value=20000
)

# ---- Personalization (UX win, low logic) ----
travel_style = st.selectbox(
    "Travel Style",
    ["Relaxed", "Adventure", "Budget", "Luxury"]
)

pace = st.slider(
    "Trip Pace",
    min_value=1,
    max_value=5,
    value=3,
    help="1 = very relaxed, 5 = tightly packed schedule"
)

# ---- Destination Row ----
place = df[df["Destination"] == destination].iloc[0]

# ---- Weather Info ----
temp, desc = get_weather(destination)
if temp:
    st.info(f"🌤 Weather in {destination}: {temp}°C, {desc.capitalize()}")

# ---- Generate Plan ----
if st.button("✨ Generate Plan"):
    rooms = math.ceil(travelers / occupancy)

    hotel_cost = place["HotelCost"] * days * rooms
    food_cost = place["FoodCost"] * days * travelers
    activity_cost = place["ActivitiesCost"] * days * travelers
    transport_cost = place["TransportCost"]

    total_estimated = hotel_cost + food_cost + activity_cost + transport_cost

    # ---- Trip Summary ----
    st.subheader("🧾 Trip Summary")
    st.markdown(f"""
    - **Destination:** {destination}  
    - **Duration:** {days} days  
    - **Travelers:** {travelers}  
    - **Travel Style:** {travel_style}  
    - **Trip Pace:** {pace}/5  
    - **Rooms Required:** {rooms}
    """)

    # ---- Cost Breakdown ----
    st.subheader("📊 Estimated Cost Breakdown")
    breakdown = {
        "Hotel (rooms × nights)": f"₹{hotel_cost:,}",
        "Food (per person × days)": f"₹{food_cost:,}",
        "Activities (per person × days)": f"₹{activity_cost:,}",
        "Transport (fixed)": f"₹{transport_cost:,}"
    }
    st.table(pd.DataFrame(breakdown.items(), columns=["Category", "Estimated Cost (₹)"]))

    st.metric("💰 Total Estimated Cost", f"₹{total_estimated:,}")

    # ---- Calculation Explanation ----
    st.subheader("🧮 Cost Calculation Details")
    st.markdown(f"""
    - **Rooms** = ceil({travelers} / {occupancy}) = **{rooms}**
    - **Hotel** = ₹{place['HotelCost']} × {days} × {rooms} = **₹{hotel_cost:,}**
    - **Food** = ₹{place['FoodCost']} × {days} × {travelers} = **₹{food_cost:,}**
    - **Activities** = ₹{place['ActivitiesCost']} × {days} × {travelers} = **₹{activity_cost:,}**
    - **Transport** = **₹{transport_cost:,}**
    ---
    **Total** = **₹{total_estimated:,}**
    """)

    # ---- Save to session_state ----
    st.session_state["trip"] = {
        "destination": destination,
        "days": days,
        "travelers": travelers,
        "occupancy": occupancy,
        "rooms": rooms,
        "estimate": total_estimated,
        "budget": budget,
        "style": travel_style,
        "pace": pace,
        "breakdown": {
            "Hotel": hotel_cost,
            "Food": food_cost,
            "Activities": activity_cost,
            "Transport": transport_cost
        }
    }

    st.session_state["expenses"] = []

    # ---- Budget Feedback ----
    if total_estimated > budget:
        st.error(f"⚠ Over Budget by ₹{total_estimated - budget:,}")
    else:
        st.success(f"✅ Within Budget! You save ₹{budget - total_estimated:,}")

    st.info("Proceed to **Manage Expenses** to track actual spending.")
