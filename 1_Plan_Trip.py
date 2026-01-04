# pages/1_Plan_Trip.py
import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Plan Trip", page_icon="🧭")

st.title("🧭 Smart Trip Planner")

# ---- Load Dataset ----
@st.cache_data
def load_tour_data():
    # Assumes india_tour_data.csv is in the same folder as app.py
    return pd.read_csv("india_tour_data.csv")

try:
    df = load_tour_data()
except FileNotFoundError:
    st.error(
        "❌ Could not find `india_tour_data.csv`.\n\n"
        "Make sure the file is in the **same folder as `app.py`** or update the path in `load_tour_data()`."
    )
    st.stop()

# ---- User Inputs ----
destination = st.selectbox("Select Destination", df["Destination"].unique())
days = st.number_input("Days of Stay", min_value=1, max_value=30, value=2)
travelers = st.number_input("Number of Travelers", min_value=1, max_value=20, value=2)

# occupancy: how many people share one room
occupancy = st.slider(
    "People per room (room occupancy)",
    min_value=1,
    max_value=4,
    value=2,
    help="Set how many people will share a room. Used to compute number of rooms."
)

budget = st.number_input(
    "Your Budget (₹)",
    min_value=1000,
    max_value=500000,
    value=20000
)

# ---- Fetch selected destination row ----
place = df[df["Destination"] == destination].iloc[0]

if st.button("Generate Plan ✨"):
    # Number of rooms needed (rounded up)
    rooms = math.ceil(travelers / occupancy)

    # Hotel cost is per ROOM per night in our dataset assumption.
    hotel_rate_per_night = place["HotelCost"]
    hotel_cost = hotel_rate_per_night * days * rooms

    # Food & activities are usually per person per day (dataset assumed)
    food_cost = place["FoodCost"] * days * travelers
    activity_cost = place["ActivitiesCost"] * days * travelers

    # Transport kept as fixed per-dataset value
    transport_cost = place["TransportCost"]

    total_estimated = hotel_cost + food_cost + activity_cost + transport_cost

    # ---- Display breakdown ----
    st.subheader("📊 Estimated Cost Breakdown")
    breakdown = {
        "Hotel (rooms × nights)": f"₹{hotel_cost:,}",
        "Food (per person × days)": f"₹{food_cost:,}",
        "Activities (per person × days)": f"₹{activity_cost:,}",
        "Transport (fixed)": f"₹{transport_cost:,}"
    }
    st.table(pd.DataFrame(breakdown.items(), columns=["Category", "Estimated Cost (₹)"]))

    st.metric("💰 Total Estimated Cost", f"₹{total_estimated:,}")

    # ---- Detailed explanation ----
    st.subheader("🧮 Cost Calculation Details")
    st.markdown(f"""
- **Number of rooms required** = ceil(travelers / occupancy) = ceil({travelers} / {occupancy}) = **{rooms} rooms**
- **Hotel Cost** = ₹{hotel_rate_per_night} × {days} days × {rooms} rooms = **₹{hotel_cost:,}**
- **Food Cost** = ₹{place['FoodCost']} × {days} days × {travelers} travelers = **₹{food_cost:,}**
- **Activities Cost** = ₹{place['ActivitiesCost']} × {days} days × {travelers} travelers = **₹{activity_cost:,}**
- **Transport (Fixed)** = **₹{transport_cost:,}**
---
**Total Estimated Cost** = {hotel_cost:,} + {food_cost:,} + {activity_cost:,} + {transport_cost:,} = **₹{total_estimated:,}**
    """)

    # ---- Save trip into session_state so other pages can use it ----
    st.session_state["trip"] = {
        "destination": destination,
        "days": days,
        "travelers": travelers,
        "occupancy": occupancy,
        "rooms": rooms,
        "estimate": total_estimated,
        "budget": budget,
        "breakdown": {
            "Hotel": hotel_cost,
            "Food": food_cost,
            "Activities": activity_cost,
            "Transport": transport_cost
        }
    }

    # Reset expenses when new trip is planned (optional)
    st.session_state["expenses"] = []

    # ---- Budget feedback ----
    if total_estimated > budget:
        st.error(f"⚠ Over Budget by ₹{total_estimated - budget:,}")
    else:
        st.success(f"✅ Within Budget! You save ₹{budget - total_estimated:,}")

    st.info("You can now track expenses from the 'Manage Expenses' page.")
