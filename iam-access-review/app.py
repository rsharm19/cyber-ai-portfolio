import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="IAM Governance Dashboard",
    layout="wide"
)

st.title("🔐 Enterprise IAM Governance Dashboard")

st.markdown("""
Analyze IAM risks, MFA compliance, dormant accounts,
privileged users, and governance findings.
""")

# =========================
# LOAD CSV
# =========================
##Adding file upload option for testing without local file access
# try:
  #   df = pd.read_csv("UsersDynamicRisk.csv")
# except FileNotFoundError:
  #   st.error("UsersDynamicRisk.csv not found.")
    # st.stop()

# df.columns = df.columns.str.strip()

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload IAM CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using default dataset: UsersDynamicRisk.csv")
    df = pd.read_csv("UsersDynamicRisk.csv")

df.columns = df.columns.str.strip()

# =========================
# DYNAMIC RISK SCORING
# =========================

def calculate_risk(row):

    score = 0

    role = str(row["role"]).lower()

    privileged_keywords = [
    "admin",
    "administrator",
    "root",
    "dba",
    "security",
    "privileged",
    "break glass",
    "breakglass",
    "cyberark",
    "sailpoint",
    "saviynt",
    "production support",
    "global"
]

    if any(keyword in role for keyword in privileged_keywords):
     score += 40

    # MFA Disabled
    if row["MFA_enabled"] == "No":
        score += 25

    # Inactive Account
    if row["status"] == "Inactive":
        score += 20

    # Contractor
    if row["account_type"] == "Contractor":
        score += 10

    # Service Account
    if row["account_type"] == "Service":
        score += 15

    # Dormant Account
    try:
        if int(row["last_login_days"]) > 90:
            score += 20
    except:
        pass

    # Shared Account
    if "shared" in str(row["username"]).lower():
        score += 15

    return min(score, 100)

# Calculate Risk Score
df["risk_score"] = df.apply(calculate_risk, axis=1)

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

# =========================
# SEARCH & FILTER
# =========================

st.sidebar.header("Filters")

search = st.sidebar.text_input(
    "Search Username"
)

severity_filter = st.sidebar.selectbox(
    "Filter by Severity",
    ["All", "Critical", "High", "Medium", "Low"]
)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["username"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

if severity_filter != "All":
    filtered_df = filtered_df[
        filtered_df["severity"] == severity_filter
    ]

# =========================
# METRICS
# =========================

critical_users = len(
    df[df["severity"] == "Critical"]
)

mfa_issues = len(
    df[df["MFA_enabled"] == "No"]
)

inactive_accounts = len(
    df[df["status"] == "Inactive"]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Critical Users",
    critical_users
)

col2.metric(
    "MFA Issues",
    mfa_issues
)

col3.metric(
    "Inactive Accounts",
    inactive_accounts
)

# =========================
# SEVERITY CHART
# =========================

st.subheader("📊 Severity Distribution")

severity_counts = df["severity"].value_counts()

st.bar_chart(severity_counts)

# =========================
# IAM RISK REPORT
# =========================

st.subheader("📋 IAM Risk Report")

st.write(
    f"Showing {len(filtered_df)} user(s)"
)

st.dataframe(
    filtered_df[
        [
            "username",
            "role",
            "risk_score",
            "severity",
            "MFA_enabled",
            "status"
        ]
    ],
    use_container_width=True
)

# =========================
# CRITICAL ACCOUNTS
# =========================

st.subheader("🚨 Critical Accounts")

critical_df = df[
    df["severity"] == "Critical"
]

if len(critical_df) > 0:
    st.dataframe(
        critical_df,
        use_container_width=True
    )
else:
    st.success(
        "No Critical Accounts Found"
    )

# =========================
# FULL DATASET
# =========================

with st.expander("View Full Dataset"):
    st.dataframe(
        df,
        use_container_width=True
    )

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption(
    "IAM Governance Dashboard | Python + Streamlit"
)