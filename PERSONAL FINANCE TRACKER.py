import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state variables
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date', 'Type', 'Amount', 'Category'])

# Title and description
st.title("Personal Finance Tracker")
st.write("Track your income and expenses, visualize your spending patterns, and set budget goals.")

# Sidebar for input
st.sidebar.header("Add Transaction")
date = st.sidebar.date_input("Date")
transaction_type = st.sidebar.selectbox("Type", ["Income", "Expense"])
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
category = st.sidebar.text_input("Category")

if st.sidebar.button("Add"):
    new_transaction = pd.DataFrame([[date, transaction_type, amount, category]], columns=['Date', 'Type', 'Amount', 'Category'])
    st.session_state['data'] = pd.concat([st.session_state['data'], new_transaction], ignore_index=True)
    st.sidebar.success("Transaction added!")

# Display data
st.header("Transaction History")
st.dataframe(st.session_state['data'])

# Visualization
st.header("Spending Patterns")
if not st.session_state['data'].empty:
    expenses = st.session_state['data'][st.session_state['data']['Type'] == 'Expense']
    if not expenses.empty:
        fig, ax = plt.subplots()
        expenses.groupby('Category')['Amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
    else:
        st.write("No expenses to display.")
else:
    st.write("No transactions to display.")

# Budget Goal
st.header("Set Budget Goal")
budget = st.number_input("Monthly Budget", min_value=0.0, format="%.2f")
if budget > 0:
    total_expenses = expenses['Amount'].sum() if not expenses.empty else 0.0
    remaining_budget = budget - total_expenses
    st.metric("Remaining Budget", f"${remaining_budget:.2f}")
else:
    st.write("Please set a budget goal.")

# Financial Summary
st.header("Financial Summary")
if not st.session_state['data'].empty:
    total_income = st.session_state['data'][st.session_state['data']['Type'] == 'Income']['Amount'].sum()
    total_expenses = st.session_state['data'][st.session_state['data']['Type'] == 'Expense']['Amount'].sum()
    net_savings = total_income - total_expenses
    st.metric("Total Income", f"${total_income:.2f}")
    st.metric("Total Expenses", f"${total_expenses:.2f}")
    st.metric("Net Savings", f"${net_savings:.2f}")
else:
    st.write("No transactions to summarize.")
