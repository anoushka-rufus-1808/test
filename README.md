# Smart Trip Planner

A data-driven trip planning web application built with **Python**, **Streamlit**, and **SQLite** that helps users simulate travel plans with cost and distance estimations along with user authentication and persistence.

---

## 🧠 Project Overview

**Smart Trip Planner** is an interactive travel planner that:
- Takes user trip details
- Processes structured travel data
- Estimates travel details such as cost and distance
- Manages user registration and login
- Stores user information in a local database

This project demonstrates a complete application workflow combining UI, backend logic, data storage, and modular design.

---

## 🚀 Features

- 🔐 User Authentication (Sign Up / Login)
- 📍 Trip detail collection (destination, preferences, etc.)
- 📊 Travel data processing using structured CSV data
- 🗂 Modular architecture (separate logic, UI, and database components)
- ✅ Instant result display in a clean UI
- 📁 Local database using SQLite for user data

---

## 📦 Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend / UI | **Streamlit** |
| Backend Logic | **Python** |
| Database | **SQLite** |
| Dataset | **CSV** file |

**Why these technologies?**
- **Python** for readable, maintainable logic
- **Streamlit** enables rapid UI development without heavy frontend code
- **SQLite** provides lightweight persistence without server setup
- **CSV dataset** ensures deterministic behavior without external API dependencies :contentReference[oaicite:1]{index=1}

---

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/anoushka-rufus-1808/test
2. **Navigate into the project**
    ```bash
    cd test
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
4. **Run the app**
    ```bash
    streamlit run app.py

## 🎯 How It Works

1.A user registers or logs in with credentials.

2.Once authenticated, the user enters travel details.

3.The app reads the CSV dataset to compute travel estimations.

4.Results are displayed immediately on the interface.
