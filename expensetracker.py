import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
st.set_page_config(page_title=" Expense Tracker", page_icon="💵", layout="wide")
st.markdown(
    """
    <style>
    /* Main App background */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #b3e5fc); /* light sky blue gradient */
        min-height: 100vh;
        color: #0d1b2a;
    }
    h1, h2, h3, h4 {
        color: #0d1b2a;
    }
    .stButton>button {
        background-color: #0288d1;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0277bd;
        color: #fff;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
    }
    .stDataFrame {
        background: white;
        border-radius: 10px;
    }
    /* Fix white header + toolbar */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #e0f7fa, #b3e5fc);
    }
    div[data-testid="stToolbar"] {
        background: linear-gradient(135deg, #e0f7fa, #b3e5fc);
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Monthly Expense Tracker")
if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.subheader("Add a New Expense")
with st.form("expense_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        amount = st.number_input("Amount (Rs.)", min_value=0.0, format="%.2f")
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    with col3:
        date = st.date_input("Date", datetime.date.today())

    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button(" Add Expense")

    if submitted and amount > 0:
        st.session_state.expenses.append(
            {"Date": str(date), "Category": category, "Amount": amount, "Note": note}
        )
        st.success("Expense added successfully!")
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    total = df["Amount"].sum()
    count = len(df)
    st.subheader("Expense Overview")
    c1, c2 = st.columns(2)
    c1.metric(" Total Spent", f"Rs. {total:.2f}")
    c2.metric(" Number of Entries", count)
    st.subheader("All Expenses")
    st.dataframe(df, use_container_width=True)
    st.subheader("Expense Analysis")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(df, names="Category", values="Amount",
                     title="Expenses by Category", hole=0.3,
                     color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df["Date"] = pd.to_datetime(df["Date"])
        fig2 = px.bar(df, x="Date", y="Amount", color="Category",
                      title="Daily Expenses", text_auto=True,
                      color_discrete_sequence=px.colors.sequential.Sunset)
        st.plotly_chart(fig2, use_container_width=True)
    if st.button(" Clear All Expenses"):
        st.session_state.expenses = []
        st.warning("All expenses cleared!")

else:
    st.info(" No expenses yet. Add your first one above.")
