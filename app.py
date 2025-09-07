import io
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from textblob import TextBlob
from datetime import datetime
from PIL import Image

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="🤖 AI Business Operations Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Custom Styling
# -------------------------
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: #ffffff;
        }
        h1 {
            color: #00c0f0 !important;
            text-align: center;
        }
        h2, h3 {
            color: #00e6b8 !important;
        }
        .stButton>button {
            background-color: #00c0f0;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #00e6b8;
            color: black;
        }
        .css-1d391kg, .css-1v3fvcr {
            background-color: #1e222b !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown("<h1>🤖 AI Business Operations Suite</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Your 4-in-1 AI Assistant for Smarter Workflows</h3>", unsafe_allow_html=True)
st.write("---")

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("📌 Select an Agent")
app_mode = st.sidebar.radio(
    "Choose an AI Agent:",
    ["📊 Financial Report Agent", "👥 HR Management Agent", "💬 Customer Feedback Analyzer", "📦 Order Tracking Agent"]
)

# -------------------------
# 1. Financial Report Agent
# -------------------------
if app_mode == "📊 Financial Report Agent":
    st.subheader("📊 Financial Report Agent")

    uploaded_file = st.file_uploader("Upload a financial CSV/XLSX file", type=["csv", "xlsx"])
    pasted_csv = st.text_area("Or paste CSV data here")

    if uploaded_file or pasted_csv.strip():
        try:
            if uploaded_file:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(io.StringIO(pasted_csv))

            st.write("### Preview of Uploaded Data")
            st.dataframe(df)

            st.write("### Summary Report")
            report = {
                "Total Revenue": df.iloc[:, 1].sum(),
                "Total Expenses": df.iloc[:, 2].sum(),
                "Computed Net Profit": df.iloc[:, 1].sum() - df.iloc[:, 2].sum()
            }
            st.json(report)

            st.write("### Profit & Expense Trends")
            df_plot = df.iloc[:, :3]
            df_plot.set_index(df_plot.columns[0], inplace=True)
            df_plot.plot(kind="bar", figsize=(8, 4))
            st.pyplot(plt)

            st.download_button("⬇️ Download Report (CSV)", df.to_csv(index=False), "financial_report.csv", "text/csv")
            st.download_button("⬇️ Download Report (Excel)", df.to_excel("financial_report.xlsx", index=False), "financial_report.xlsx")

        except Exception as e:
            st.error(f"Error processing file: {e}")

# -------------------------
# 2. HR Management Agent
# -------------------------
elif app_mode == "👥 HR Management Agent":
    st.subheader("👥 HR Management Agent")

    uploaded_file = st.file_uploader("Upload employee dataset (CSV/XLSX)", type=["csv", "xlsx"])
    pasted_csv = st.text_area("Or paste employee CSV data here")

    if uploaded_file or pasted_csv.strip():
        try:
            if uploaded_file:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(io.StringIO(pasted_csv))

            st.write("### Employee Data Preview")
            st.dataframe(df)

            st.write("### HR Insights")
            st.write(f"👥 Total Employees: {len(df)}")
            if "Department" in df.columns:
                st.write("📌 Employees per Department")
                st.bar_chart(df["Department"].value_counts())

            if "Salary" in df.columns:
                st.write("💰 Salary Distribution")
                st.histogram = plt.hist(df["Salary"], bins=20)
                st.pyplot(plt)

            st.download_button("⬇️ Download Employee Report (CSV)", df.to_csv(index=False), "employee_report.csv", "text/csv")

        except Exception as e:
            st.error(f"Error processing HR data: {e}")

# -------------------------
# 3. Customer Feedback Analyzer
# -------------------------
elif app_mode == "💬 Customer Feedback Analyzer":
    st.subheader("💬 Customer Feedback Analyzer")

    feedback_input = st.text_area("Paste customer feedback (one per line)")
    if feedback_input.strip():
        feedback_list = feedback_input.split("\n")
        sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
        polarity_scores = []

        for feedback in feedback_list:
            analysis = TextBlob(feedback).sentiment.polarity
            polarity_scores.append(analysis)
            if analysis > 0.1:
                sentiments["Positive"] += 1
            elif analysis < -0.1:
                sentiments["Negative"] += 1
            else:
                sentiments["Neutral"] += 1

        st.write("### Sentiment Summary")
        st.json(sentiments)

        st.write("### Sentiment Distribution")
        labels = list(sentiments.keys())
        sizes = list(sentiments.values())
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        st.pyplot(plt)

# -------------------------
# 4. Order Tracking Agent
# -------------------------
elif app_mode == "📦 Order Tracking Agent":
    st.subheader("📦 Order Tracking Agent")

    order_id = st.text_input("Enter Order ID")
    if st.button("🔍 Track Order"):
        if order_id.strip():
            # Simulated tracking system
            import random
            status = random.choice(["✅ Delivered", "🚚 Out for Delivery", "📦 In Transit", "⌛ Processing"])
            st.success(f"Order ID {order_id} Status: {status}")
            st.write(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.warning("Please enter a valid Order ID.")
