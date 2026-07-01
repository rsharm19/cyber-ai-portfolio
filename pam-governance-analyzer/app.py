import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PAM Governance Analyzer",
    layout="wide"
)

st.title("🔐 PAM Governance Analyzer")

st.write(
    "Upload a privileged account report and identify PAM governance risks."
)

# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload PAM Account CSV",
    type=["csv"]
)

# ==========================================
# PROCESS FILE
# ==========================================

if uploaded_file:

    try:
        df = pd.read_csv(uploaded_file)

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.subheader("Uploaded PAM Data")
    st.dataframe(df)

    # ======================================
    # VALIDATE REQUIRED COLUMNS
    # ======================================

    required_columns = [
        "username",
        "account_type",
        "system",
        "mfa_enabled",
        "last_login_days",
        "status"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        st.error(
            f"Missing columns: {', '.join(missing_columns)}"
        )

        st.stop()

    # ======================================
    # RISK SCORING FUNCTION
    # ======================================

    def calculate_risk(row):

        score = 0

        # MFA Risk
        if str(row["mfa_enabled"]).lower() == "no":
            score += 30

        # Dormant Account Risk
        if int(row["last_login_days"]) > 90:
            score += 30

        # Shared Account Risk
        if "shared" in str(row["username"]).lower():
            score += 20

        # Inactive Account Risk
        if str(row["status"]).lower() == "inactive":
            score += 20

        return min(score, 100)

    df["risk_score"] = df.apply(
        calculate_risk,
        axis=1
    )

    # ======================================
    # RISK LEVEL FUNCTION
    # ======================================

    def classify_risk(score):

        if score >= 80:
            return "Critical"

        elif score >= 60:
            return "High"

        elif score >= 30:
            return "Medium"

        else:
            return "Low"

    df["risk_level"] = df["risk_score"].apply(
        classify_risk
    )

    # ======================================
    # FINDINGS ENGINE
    # ======================================

    findings = []

    mfa_issues = 0
    dormant_accounts = 0
    shared_accounts = 0
    inactive_accounts = 0

    for _, row in df.iterrows():

        username = row["username"]

        if str(row["mfa_enabled"]).lower() == "no":

            findings.append(
                f"{username} does not have MFA enabled"
            )

            mfa_issues += 1

        if int(row["last_login_days"]) > 90:

            findings.append(
                f"{username} is dormant"
            )

            dormant_accounts += 1

        if "shared" in str(username).lower():

            findings.append(
                f"{username} is a shared privileged account"
            )

            shared_accounts += 1

        if str(row["status"]).lower() == "inactive":

            findings.append(
                f"{username} is inactive"
            )

            inactive_accounts += 1

    # ======================================
    # PAM RISK METRICS
    # ======================================

    st.subheader("📊 PAM Risk Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "MFA Issues",
        mfa_issues
    )

    col2.metric(
        "Dormant Accounts",
        dormant_accounts
    )

    col3.metric(
        "Shared Accounts",
        shared_accounts
    )

    col4.metric(
        "Inactive Accounts",
        inactive_accounts
    )

    # ======================================
    # RISK DISTRIBUTION
    # ======================================

    st.subheader("📈 Risk Distribution")

    risk_counts = (
        df["risk_level"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(risk_counts)

    # ======================================
    # PAM RISK ANALYSIS TABLE
    # ======================================

    st.subheader("🔍 PAM Risk Analysis")

    st.dataframe(
        df[
            [
                "username",
                "account_type",
                "system",
                "risk_score",
                "risk_level"
            ]
        ]
    )

    # ======================================
    # FILTER BY RISK LEVEL
    # ======================================

    st.subheader("🎯 Filter by Risk Level")

    selected_risk = st.selectbox(
        "Select Risk Level",
        ["All", "Critical", "High", "Medium", "Low"]
    )

    if selected_risk != "All":

        filtered_df = df[
            df["risk_level"] == selected_risk
        ]

    else:

        filtered_df = df

    st.dataframe(
        filtered_df[
            [
                "username",
                "account_type",
                "system",
                "risk_score",
                "risk_level"
            ]
        ]
    )

    # ======================================
    # PAM FINDINGS
    # ======================================

    st.subheader("🚨 PAM Findings")

    if findings:

        for finding in findings:

            st.write("•", finding)

    else:

        st.success(
            "No significant PAM risks detected."
        )

    # ======================================
    # RECOMMENDATIONS
    # ======================================

    st.subheader("✅ PAM Governance Recommendations")

    recommendations = []

    if mfa_issues > 0:

        recommendations.append(
            "Enable MFA for all privileged accounts."
        )

    if dormant_accounts > 0:

        recommendations.append(
            "Review and disable dormant privileged accounts."
        )

    if shared_accounts > 0:

        recommendations.append(
            "Replace shared privileged accounts with named accounts."
        )

    if inactive_accounts > 0:

        recommendations.append(
            "Remove inactive privileged users from PAM scope."
        )

    if len(
        df[df["risk_level"] == "Critical"]
    ) > 0:

        recommendations.append(
            "Conduct immediate review of Critical PAM accounts."
        )

    if recommendations:

        for rec in recommendations:

            st.success(rec)

    else:

        st.success(
            "No remediation actions required."
        )