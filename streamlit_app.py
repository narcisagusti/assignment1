import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials



scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

SHEET_NAME = "data assignment1"
sheet = client.open(SHEET_NAME).sheet1

data = pd.DataFrame(sheet.get_all_records())

st.write("✅ Data Loaded Successfully")
st.dataframe(data)

# Set up page title
st.title("What are the survivors of the titanic in each class?")

# Connect to Google Sheets
conn = st.experimental_connection("gsheets", type="gspread")
data = conn.read(ttl="2m")
st.write(data)

# Rename columns to match what your visualization code expects
data = data.rename(columns={"Class": "class", "Survivors": "count"})

# Initialize session state to track time and button visibility
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'show_answer_button' not in st.session_state:
    st.session_state.show_answer_button = False
if 'chart_shown' not in st.session_state:
    st.session_state.chart_shown = False

# First button to display random chart
if st.button("Click to display graph"):
    st.session_state.start_time = time.time()
    st.session_state.show_answer_button = True
    st.session_state.chart_shown = True
    
    # Create visualizations
    graph = random.choice([1, 2])
    
    if graph == 1:
        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(data["count"], labels=data["class"], autopct="%1.1f%%", colors=["blue", "green", "red"])
        ax.set_title("Survivors by Class (Pie Chart)")
        st.pyplot(fig)
    elif graph == 2:
        # Bar chart
        fig, ax = plt.subplots()
        ax.bar(data["class"], data["count"], color=["blue", "green", "red"])
        ax.set_title("Survivors by Class (Bar Chart)")
        ax.set_xlabel("Class")
        ax.set_ylabel("Count")
        st.pyplot(fig)

# Only show the answer button after a chart has been displayed
if st.session_state.show_answer_button:
    if st.button("I answered your question"):
        end_time = time.time()
        time_taken = end_time - st.session_state.start_time
        st.write(f"It has taken you {time_taken:.2f} seconds to answer the question")
        # Reset for next attempt
        st.session_state.show_answer_button = False
        st.session_state.chart_shown = False