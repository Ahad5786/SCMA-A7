import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import os

# Set the page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load and display the logo image if it exists
logo_path = "logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=150)

# Title of the app
st.title("Personal Finance Tracker")

# Introduction
st.markdown("""
Welcome to your Personal Finance Tracker! This app helps you monitor your income, expenses, and investments over the year.
""")

# Load the data
@st.cache_data
def load_data():
    income_data = pd.read_csv("income_data.csv")
    expenses_data = pd.read_csv("expenses_data.csv")
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

# Calculate total savings
total_savings = combined_data["Savings"].sum()

# Display total savings
st.metric("Total Savings", f"${total_savings:,.2f}")

# Plotting
st.subheader("Monthly Income, Expenses, and Savings")

# Altair chart for Income and Expenses
income_expenses_chart = alt.Chart(combined_data).mark_bar().encode(
    x=alt.X('Month', sort=None),
    y=alt.Y('value', title='Amount'),
    color=alt.Color('variable', legend=alt.Legend(title="Legend")),
    column=alt.Column('variable', header=alt.Header(title=""))
).transform_fold(
    fold=['Income', 'Expenses']
).properties(
    width=200,
    height=300
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_header(
    titleFontSize=16,
    labelFontSize=14
)

# Altair chart for Savings
savings_chart = alt.Chart(combined_data).mark_line(point=True).encode(
    x=alt.X('Month', sort=None),
    y=alt.Y('Savings', title='Savings'),
    color=alt.value('green')
).properties(
    width=600,
    height=300
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

# Display the charts
st.altair_chart(income_expenses_chart, use_container_width=True)
st.altair_chart(savings_chart, use_container_width=True)

# Footer
st.markdown("""
---
**Developed by Ahad Zifain Miyanji**
""")
