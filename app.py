import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# ---------- Page Config ----------
st.set_page_config(page_title="AI Business Operations Suite", layout="wide")

# ---------- Main Dashboard Header ----------
st.markdown(
    """
    <div style="
        text-align:center; 
        padding: 30px; 
        border-radius: 12px;
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    ">
        <h1 style="color:white; font-size:42px; margin-bottom:5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            🤖 AI Suite
        </h1>
        <h2 style="color:#facc15; font-size:28px; margin:5px 0;">
            AI Business Operations Suite
        </h2>
        <p style="color:#e0e7ff; font-size:18px; margin-top:0;">
            Your 4-in-1 AI Assistant for Smarter Workflows
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# ---------- Sidebar Navigation ----------
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("Select an AI Agent below to get started:")

try:
    st.sidebar.image("logo.png", width=80)
except Exception:
    st.sidebar.markdown("🤖")

agent = st.sidebar.selectbox(
    "Agents",
    [
        "Automating Financial Reporting",
        "Handling FAQs (Customer Service)",
        "Customer Feedback Analysis",
        "Order Status Tracking"
    ],
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Powered by the AI Business Operations Suite")

# ---------- Agent 1: Financial Reporting ----------
if agent == "Automating Financial Reporting":
    st.header("📊 Automating Financial Reporting")
    st.write("Upload a financial dataset (CSV) to generate reports automatically.")
    
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Data")
        st.dataframe(df)

        if "Revenue" in df.columns and "Expenses" in df.columns:
            df["Profit"] = df["Revenue"] - df["Expenses"]
            st.subheader("Summary Report")
            st.write(df.describe())

            # Plot
            st.subheader("Revenue vs Expenses")
            fig, ax = plt.subplots()
            df.plot(x="Date", y=["Revenue", "Expenses", "Profit"], ax=ax, marker="o")
            st.pyplot(fig)

            # Download button
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Report", csv, "financial_report.csv", "text/csv")

# ---------- Agent 2: FAQs ----------
elif agent == "Handling FAQs (Customer Service)":
    st.header("💬 Customer Service FAQ Agent")
    st.write("Upload a FAQ knowledge base (CSV with 'question' and 'answer' columns) or type your question manually.")

    uploaded_file = st.file_uploader("Upload FAQ CSV", type=["csv"])
    question = st.text_area("❓ Enter your question here")

    if uploaded_file:
        faq_df = pd.read_csv(uploaded_file)
        if st.button("Get Answer"):
            answer = None
            for i, row in faq_df.iterrows():
                if question.lower() in row["question"].lower():
                    answer = row["answer"]
                    break
            if answer:
                st.success(answer)
            else:
                st.warning("Sorry, I couldn't find an answer to your question.")

# ---------- Agent 3: Customer Feedback Analysis ----------
elif agent == "Customer Feedback Analysis":
    st.header("📝 Customer Feedback Analysis")
    st.write("Upload customer feedback (CSV with a 'Feedback' column) to analyze sentiment.")

    uploaded_file = st.file_uploader("Upload Feedback CSV", type=["csv"])
    feedback_text = st.text_area("✍️ Or paste feedback here")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Feedback Data")
        st.dataframe(df)

        if "Feedback" in df.columns:
            st.subheader("Sentiment Analysis")
            df["Sentiment"] = df["Feedback"].apply(lambda x: TextBlob(x).sentiment.polarity)
            df["SentimentLabel"] = df["Sentiment"].apply(
                lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral")
            )
            st.dataframe(df[["Feedback", "SentimentLabel"]])

            # Plot
            st.subheader("Sentiment Distribution")
            fig, ax = plt.subplots()
            df["SentimentLabel"].value_counts().plot(kind="bar", ax=ax)
            st.pyplot(fig)

    elif feedback_text:
        sentiment = TextBlob(feedback_text).sentiment.polarity
        label = "Positive" if sentiment > 0 else ("Negative" if sentiment < 0 else "Neutral")
        st.info(f"Sentiment: **{label}** (Score: {sentiment:.2f})")

# ---------- Agent 4: Order Status Tracking ----------
elif agent == "Order Status Tracking":
    st.header("📦 Order Status Tracking")
    st.write("Upload order data (CSV with 'OrderID' and 'Status' columns) or enter an Order ID manually.")

    uploaded_file = st.file_uploader("Upload Orders CSV", type=["csv"])
    order_id = st.text_input("🔎 Enter Order ID")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Orders")
        st.dataframe(df)

        if order_id:
            match = df[df["OrderID"] == order_id]
            if not match.empty:
                status = match.iloc[0]["Status"]
                st.success(f"✅ Order {order_id} status: {status}")
            else:
                st.error("Order ID not found.")
