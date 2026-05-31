import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(page_title="IAM Dashboard")

st.title("🔐 Enterprise IAM Governance Dashboard")


# =========================
# LOAD CSV
# =========================

# df = pd.read_csv("enterprise_users.csv", sep=",") -- Removed to add file uploader
uploaded_file = st.file_uploader(
    "Upload IAM CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    from pathlib import Path
    csv_file = Path(__file__).parent / "enterprise_users.csv"
    df = pd.read_csv(csv_file)
   # df = pd.read_csv("enterprise_users.csv")

df.columns = df.columns.str.strip()

# =========================
# SHOW DATAFRAME
# =========================

## Removed below 2 lines to add search and filter functionality

#st.subheader("IAM Dataset")

#st.dataframe(df)


# =========================
# RISK CLASSIFICATION
# =========================

def classify_risk(score):

    if score >= 90:
        return "Critical"

    elif score >= 70:
        return "High"

    elif score >= 40:
        return "Medium"

    else:
        return "Low"


df["severity"] = df["risk_score"].apply(classify_risk)
# Search box
search = st.text_input("Search Username")

# Severity filter
severity_filter = st.selectbox(
    "Filter by Severity",
    ["All", "Critical", "High", "Medium", "Low"]
)

# Apply filters
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["username"].str.contains(search, case=False)
    ]

if severity_filter != "All":
    filtered_df = filtered_df[
        filtered_df["severity"] == severity_filter
    ]

# SHOW FILTERED RESULTS
st.subheader("IAM Risk Report")

st.write(f"Showing {len(filtered_df)} user(s)")

st.dataframe(filtered_df)

# =========================
# METRICS
# =========================

critical_users = len(df[df["severity"] == "Critical"])

mfa_issues = len(df[df["MFA_enabled"] == "No"])

inactive_accounts = len(df[df["status"] == "Inactive"])


col1, col2, col3 = st.columns(3)

col1.metric("Critical Users", critical_users)

col2.metric("MFA Issues", mfa_issues)

col3.metric("Inactive Accounts", inactive_accounts)


# =========================
# CHART
# =========================

st.subheader("Severity Distribution")

severity_counts = df["severity"].value_counts()

st.bar_chart(severity_counts)


# =========================
# CRITICAL USERS
# =========================

st.subheader("Critical Accounts")

critical_df = df[df["severity"] == "Critical"]

st.dataframe(critical_df)