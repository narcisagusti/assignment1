import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(ttl="2m")

# Rename columns to match what your code is expecting
data = data.rename(columns={"Class": "class", "Survivors": "count"})

st.title("What are the survivors of the titanic in each class?")

# Create visualizations
pie_chart, ax = plt.subplots()
ax.pie(data["count"], labels=data["class"], autopct="%1.1f%%", colors=["blue", "green", "red"])
ax.set_title("Survivors by Class (Pie Chart)")

bar_chart, ax = plt.subplots()
ax.bar(data["class"], data["count"], color=["blue", "green", "red"])
ax.set_title("Survivors by Class (Bar Chart)")
ax.set_xlabel("Class")
ax.set_ylabel("Count")

# Display buttons and handle interaction
random_button = st.button("Click to display graph")
start_time = 0

if random_button:
    start_time = time.time()
    graph = random.choice([1, 2])
    if graph == 1:
        st.pyplot(pie_chart)
    elif graph == 2:
        st.pyplot(bar_chart)

answer = st.button("Question answered")
if answer and start_time > 0:
    end_time = time.time()
    time_taken = end_time - start_time
    st.write(f"It has taken you {time_taken:.2f} seconds to answer the question")