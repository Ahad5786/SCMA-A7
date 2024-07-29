import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Set the page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title of the app
st.title("Personal Finance Tracker")

# Introduction
st.markdown("""
Welcome to your Personal Finance Tracker! This app helps you monitor your income, expenses, and investments over the year.
""")

# Load the data
@st.cache_data
def load_data():
    # Placeholder data since we are not using actual CSV files
    income_data = pd.DataFrame({
        "Month": ["January", "February", "March"],
        "Income": [4000, 4200, 4300]
    })
    
    expenses_data = pd.DataFrame({
        "Month": ["January", "February", "March"],
        "Expenses": [3200, 3500, 3300]
    })
    return income_data, expenses_data

income_data, expenses_data = load_data()

# Display the data
st.sidebar.header("Data")
st.sidebar.write("Income Data", income_data)
st.sidebar.write("Expenses Data", expenses_data)

# Combine the data into a single DataFrame
combined_data = pd.merge(income_data, expenses_data, on="Month")

# Calculate savings
combined_data["Savings"] = combined_data["Income"] - combined_data["Expenses"]

# Display the combined data
st.write("Combined Data", combined_data)

# Visualize the data
st.header("Visualizations")

# Line chart for income and expenses
line_chart = alt.Chart(combined_data).mark_line().encode(
    x="Month",
    y=alt.Y("Income", title="Amount"),
    color=alt.value("blue")
).interactive()

line_chart += alt.Chart(combined_data).mark_line().encode(
    x="Month",
    y=alt.Y("Expenses", title="Amount"),
    color=alt.value("red")
).interactive()

st.altair_chart(line_chart, use_container_width=True)

# Bar chart for savings
bar_chart = alt.Chart(combined_data).mark_bar().encode(
    x="Month",
    y="Savings",
    color=alt.value("green")
).interactive()

st.altair_chart(bar_chart, use_container_width=True)

# Footer
st.markdown("""
**Developed by Ahad Zifain Miyanji**

For more information, contact me at [ahadzifain2028@gmail.com](mailto:ahadzifain2028@gmail.com)
""")
