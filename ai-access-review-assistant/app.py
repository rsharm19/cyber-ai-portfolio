import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Access Review Assistant",
    layout="wide"
)

st.title("🤖 AI Access Review Assistant")
st.write(
    "Upload an IAM Access Review CSV and generate a security assessment report."
)

# ==========================================
# AI ASSESSMENT FUNCTION
# ==========================================

def generate_assessment(findings):

    critical_count = 0

    for finding in findings:

        if (
            "privileged" in finding.lower()
            or "inactive" in finding.lower()
            or "dormant" in finding.lower()
        ):
            critical_count += 1

    if critical_count >= 4:
        risk_level = "Critical"

    elif critical_count >= 2:
        risk_level = "High"

    else:
        risk_level = "Medium"

    report = f"""
=================================
AI ACCESS REVIEW ASSESSMENT
=================================

Risk Level: {risk_level}

Summary:
Identity governance risks detected during access review.

Key Findings:
"""

    for item in findings:
        report += f"\n• {item}"

    # Dynamic Recommendations

    recommendations = []

    if any("mfa" in item.lower() for item in findings):
        recommendations.append(
            "Enable MFA immediately for affected accounts."
        )

    if any("dormant" in item.lower() for item in findings):
        recommendations.append(
            "Disable or review dormant accounts."
        )

    if any("privileged" in item.lower() for item in findings):
        recommendations.append(
            "Conduct privileged access certification."
        )

    if any("inactive" in item.lower() for item in findings):
        recommendations.append(
            "Remove inactive accounts from critical systems."
        )

    report += "\n\nRecommendations:\n"

    for rec in recommendations:
        report += f"\n• {rec}"

        current_date = datetime.now().strftime("%Y-%m-%d")

    report += f"""

    Total Findings: {len(findings)}

    Assessment Date: {current_date}
=================================
"""
    return report
# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Access Review CSV",
    type=["csv"]
)

# ==========================================
# PROCESS FILE
# ==========================================

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    df.columns = df.columns.str.strip()

    st.subheader("Uploaded Dataset")

    st.dataframe(df)

    # ======================================
    # COLUMN VALIDATION
    # ======================================

    required_columns = [
        "username",
        "role",
        "status",
        "MFA_enabled",
        "account_type",
        "last_login_days"
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
    # FINDINGS ENGINE
    # ======================================

    findings = []

    privileged_count = 0
    inactive_count = 0
    mfa_issues = 0
    dormant_count = 0

    for _, row in df.iterrows():

        username = row["username"]

        # MFA Check

        if str(row["MFA_enabled"]).lower() == "no":

            findings.append(
                f"{username} does not have MFA enabled"
            )

            mfa_issues += 1

        # Inactive Check

        if str(row["status"]).lower() == "inactive":

            findings.append(
                f"{username} is inactive"
            )

            inactive_count += 1

        # Privileged Role Check

        role = str(row["role"]).lower()

        privileged_keywords = [
            "admin",
            "administrator",
            "root",
            "cyberark",
            "sailpoint",
            "saviynt",
            "security",
            "dba",
            "global"
        ]

        if any(keyword in role for keyword in privileged_keywords):

            findings.append(
                f"{username} has privileged access"
            )

            privileged_count += 1

        # Dormant Account Check

        if int(row["last_login_days"]) > 90:

            findings.append(
                f"{username} is dormant"
            )

            dormant_count += 1

    # ======================================
    # METRICS
    # ======================================

    st.subheader("Risk Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Privileged Accounts",
        privileged_count
    )

    col2.metric(
        "MFA Issues",
        mfa_issues
    )

    col3.metric(
        "Inactive Accounts",
        inactive_count
    )

    col4.metric(
        "Dormant Accounts",
        dormant_count
    )

    # ======================================
    # FINDINGS
    # ======================================

    st.subheader("IAM Findings")

    if findings:

        for item in findings:

            st.write("•", item)

    else:

        st.success(
            "No significant IAM risks detected."
        )

    # ======================================
    # AI REPORT
    # ======================================

    if st.button("Generate AI Assessment"):

        report = generate_assessment(findings)

        st.subheader("AI Security Assessment")

        st.text(report)

        st.download_button(
            label="Download Report",
            data=report,
            file_name="AI_Access_Review_Report.txt",
            mime="text/plain"
        )