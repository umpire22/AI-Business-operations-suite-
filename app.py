# app.py
import io
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from textblob import TextBlob
from datetime import datetime

# ---------- Page config ----------
st.set_page_config(page_title="AI Business Operations Suite", layout="wide", initial_sidebar_state="expanded")

# ---------- Global styling (dark theme + colorful headers) ----------
st.markdown(
    """
    <style>
    /* Page background and text */
    .reportview-container, .main, header, .stApp {
        background-color: #0f1720;
        color: #e6eef8;
    }
    /* Card-like container */
    .card {
        background: #0b1220;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
        border: 1px solid rgba(255,255,255,0.03);
        margin-bottom: 20px;
    }
    /* Bold colorful headers */
    .agent-title {
        font-size:28px;
        font-weight:800;
        color: #7dd3fc; /* cyan */
    }
    .agent-sub {
        font-size:16px;
        font-weight:700;
        color: #fbcfe8; /* pink */
    }
    /* Buttons */
    .stButton>button {
        background-image: linear-gradient(90deg,#06b6d4,#7c3aed);
        color: white;
        font-weight: 800;
        border-radius: 8px;
        padding: 8px 14px;
    }
    /* Inputs */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div {
        background-color:#071029;
        color: #e6eef8;
        border-radius: 6px;
        padding: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# ---------- Sidebar ----------
st.sidebar.title("📌 Agents")
agent = st.sidebar.selectbox(
    "Choose an agent",
    [
        "Automating Financial Reporting",
        "Handling FAQs (Customer Service)",
        "Customer Feedback Analysis",
        "Order Status Tracking"
    ],
)
st.sidebar.markdown("---")
st.sidebar.markdown("Built with Streamlit • Professional Demo")

# ---------- Helper: convert df to CSV bytes ----------
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')

# ---------- Agent 1: Automating Financial Reporting ----------
if agent == "Automating Financial Reporting":
    st.markdown('<div class="agent-title">💰 Automating Financial Reporting Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-sub">Generate summaries, charts and downloadable reports from your financial data.</div>', unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Financial Data (CSV or XLSX)", type=["csv", "xlsx"])
    manual_input = st.expander("Or paste CSV text here (copy-paste) — optional")
    pasted_csv = manual_input.text_area("Paste CSV content (optional)", height=150)

    df = None
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Could not read the file: {e}")
    elif pasted_csv.strip() != "":
        try:
            df = pd.read_csv(io.StringIO(pasted_csv))
        except Exception as e:
            st.error(f"Could not parse pasted CSV: {e}")

    if df is not None:
        st.markdown("### 📊 Data Preview")
        st.dataframe(df.head())

        # Column mapping
        mapping = {"revenue": None, "expenses": None, "profit": None}
        for c in df.columns:
            lc = c.lower()
            if "revenue" in lc or "income" in lc or "sales" in lc:
                mapping["revenue"] = c
            if "expense" in lc or "cost" in lc:
                mapping["expenses"] = c
            if "profit" in lc or "net" in lc:
                mapping["profit"] = c

        col1 = st.selectbox("Revenue column", options=["-- none --"] + list(df.columns), index=0 if mapping["revenue"] is None else list(df.columns).index(mapping["revenue"]) + 1)
        col2 = st.selectbox("Expenses column", options=["-- none --"] + list(df.columns), index=0 if mapping["expenses"] is None else list(df.columns).index(mapping["expenses"]) + 1)
        col3 = st.selectbox("Profit column (optional)", options=["-- none --"] + list(df.columns), index=0 if mapping["profit"] is None else list(df.columns).index(mapping["profit"]) + 1)

        if st.button("Generate Financial Report"):
            report = {}
            try:
                if col1 != "-- none --":
                    report['Total Revenue'] = float(df[col1].sum())
                if col2 != "-- none --":
                    report['Total Expenses'] = float(df[col2].sum())
                if col3 != "-- none --":
                    report['Total Profit (from column)'] = float(df[col3].sum())
                if col3 == "-- none --" and col1 != "-- none --" and col2 != "-- none --":
                    report['Computed Net Profit'] = float(df[col1].sum() - df[col2].sum())

                st.markdown("### 📑 Summary")
                for k, v in report.items():
                    st.write(f"**{k}:** {v:,.2f}")

                if col1 != "-- none --" and col2 != "-- none --":
                    st.markdown("### 📈 Revenue vs Expenses")
                    fig, ax = plt.subplots(figsize=(8, 4))
                    df_plot = df[[col1, col2]].fillna(0)
                    df_plot.plot(kind="bar", ax=ax)
                    ax.set_xlabel("Record Index")
                    ax.set_ylabel("Amount")
                    ax.legend([col1, col2])
                    st.pyplot(fig)

                out_df = pd.DataFrame([report])
                st.download_button("Download Summary CSV", data=df_to_csv_bytes(out_df), file_name="financial_summary.csv", mime="text/csv")
                df_out = df.copy()
                df_out['report_generated_at'] = datetime.utcnow().isoformat()
                st.download_button("Download Enriched Data (CSV)", data=df_to_csv_bytes(df_out), file_name="financial_enriched.csv", mime="text/csv")
                st.success("Report generated successfully ✅")
            except Exception as e:
                st.error(f"Failed to generate report: {e}")
    else:
        st.info("Upload a CSV or paste CSV content to begin. A sample financial CSV should have columns like Revenue, Expenses, Profit.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Agent 2: Handling FAQs ----------
elif agent == "Handling FAQs (Customer Service)":
    st.markdown('<div class="agent-title">🤖 Handling FAQs (Customer Service)</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-sub">Fast keyword-based FAQ responses with copy & download options.</div>', unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("### Ask a question or paste many questions (one per line) below:")
    user_question = st.text_input("Type your question (e.g., What are your working hours?)")
    bulk_questions = st.text_area("Or paste multiple questions (one per line) — optional", height=120)

    faq_responses = {
        "hours": "Our customer service hours are Monday to Friday, 9 AM to 5 PM (local time).",
        "return": "You can return items within 30 days of purchase with a valid receipt.",
        "shipping": "We offer free shipping for orders over $50. Standard shipping takes 3–7 business days.",
        "payment": "We accept Visa, Mastercard and PayPal.",
        "refund": "Refunds are processed within 5–10 business days after items are received."
    }

    def find_faq_answer(q: str):
        q_l = q.lower()
        for k, v in faq_responses.items():
            if k in q_l:
                return v
        return "Sorry, I couldn't find an answer to your question."

    if user_question:
        ans = find_faq_answer(user_question)
        st.markdown("### 📝 Answer")
        st.write(ans)
        st.text_area("Copy this answer:", value=ans, height=120)
        st.download_button("Download Answer", data=ans, file_name="faq_answer.txt", mime="text/plain")

    if bulk_questions.strip() != "":
        qs = [q.strip() for q in bulk_questions.splitlines() if q.strip()]
        results = [{"question": q, "answer": find_faq_answer(q)} for q in qs]
        df_res = pd.DataFrame(results)
        st.markdown("### 📚 Bulk Results")
        st.dataframe(df_res)
        st.download_button("Download bulk FAQ answers (CSV)", data=df_to_csv_bytes(df_res), file_name="bulk_faq_answers.csv", mime="text/csv")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Agent 3: Customer Feedback Analysis ----------
elif agent == "Customer Feedback Analysis":
    st.markdown('<div class="agent-title">💬 Customer Feedback Analysis Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-sub">Sentiment analysis for individual or bulk feedback with charts and export.</div>', unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("### Paste a single review or upload a CSV with a 'feedback' column.")
    feedback_single = st.text_area("Enter single customer feedback (or leave empty)", height=120)
    uploaded_file = st.file_uploader("Upload CSV with 'feedback' column (optional)", type=["csv", "xlsx"])

    df = None
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Could not read file: {e}")

    if feedback_single.strip() != "":
        blob = TextBlob(feedback_single)
        polarity = blob.sentiment.polarity
        if polarity > 0.05:
            label = "Positive"
        elif polarity < -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        st.markdown("### 📝 Sentiment Result (Single)")
        st.write(f"**Sentiment:** {label}")
        st.write(f"**Score (polarity):** {polarity:.3f}")
        st.text_area("Copy the feedback here:", value=feedback_single, height=120)
        st.download_button("Download result (TXT)", data=f"Feedback: {feedback_single}\nSentiment: {label}\nScore: {polarity:.3f}", file_name="feedback_analysis.txt", mime="text/plain")

    if df is not None:
        if "feedback" not in [c.lower() for c in df.columns]:
            st.error("CSV must contain a 'feedback' column (case-insensitive).")
        else:
            feedback_col = [c for c in df.columns if c.lower() == "feedback"][0]
            st.markdown("### Bulk analysis preview")
            st.dataframe(df[[feedback_col]].head())

            if st.button("Analyze Feedback (Bulk)"):
                sentiments = []
                for text in df[feedback_col].astype(str).fillna(""):
                    pol = TextBlob(text).sentiment.polarity
                    if pol > 0.05:
                        lab = "Positive"
                    elif pol < -0.05:
                        lab = "Negative"
                    else:
                        lab = "Neutral"
                    sentiments.append({"feedback": text, "polarity": pol, "label": lab})
                res_df = pd.DataFrame(sentiments)
                st.markdown("### 📊 Summary")
                counts = res_df['label'].value_counts().reindex(['Positive', 'Neutral', 'Negative']).fillna(0).astype(int)
                st.write(counts.to_dict())
                fig1, ax1 = plt.subplots(figsize=(4,4))
                ax1.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=140)
                ax1.axis('equal')
                st.pyplot(fig1)
                st.markdown("### 🔍 Detailed Results")
                st.dataframe(res_df)
                st.download_button("Download feedback analysis (CSV)", data=df_to_csv_bytes(res_df), file_name="feedback_analysis.csv", mime="text/csv")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Agent 4: Order Status Tracking ----------
elif agent == "Order Status Tracking":
    st.markdown('<div class="agent-title">📦 Order Status Tracking Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-sub">Enter Order IDs and get simulated stage updates. Supports batch CSV import.</div>', unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    order_id = st.text_input("Order ID (e.g., ORD-2025-00123)")
    uploaded_file = st.file_uploader("Upload CSV with order_id column (optional)", type=["csv", "xlsx"])

    status_flow = ["Processing", "Shipped - in transit", "Out for delivery", "Delivered"]

    def simulate_status(order_id_text: str):
        if not order_id_text:
            return None
        idx = sum(ord(c) for c in str(order_id_text)) % len(status_flow)
        return status_flow[idx]

    if order_id:
        status = simulate_status(order_id)
        st.markdown("### 📦 Order Status")
        st.write(f"**Order ID:** {order_id}")
        st.write(f"**Status:** {status}")
        st.download_button("Download Order Status", data=f"Order ID: {order_id}\nStatus: {status}", file_name=f"{order_id}_status.txt", mime="text/plain")

    if uploaded_file is not None:
        try:
            df_orders = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            if "order_id" not in [c.lower() for c in df_orders.columns]:
                st.error("CSV must have an 'order_id' column (case-insensitive).")
            else:
                col = [c for c in df_orders.columns if c.lower() == "order_id"][0]
                df_orders['status'] = df_orders[col].astype(str).apply(simulate_status)
                st.markdown("### Batch Results")
                st.dataframe(df_orders[[col, 'status']].head(50))
                st.download_button("Download batch statuses (CSV)", data=df_to_csv_bytes(df_orders[[col, 'status']]), file_name="order_statuses.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Could not read file: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
