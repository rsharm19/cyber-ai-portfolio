import pandas as pd

# Read CSV
df = pd.read_csv(
    r"C:\cyber-ai-portfolio\ai-access-review-assistant\sample_access_review.csv"
)

findings = []

# Analyze users
for _, row in df.iterrows():

    if row["MFA_enabled"] == "No":
        findings.append(
            f"{row['username']} does not have MFA enabled"
        )

    if row["status"] == "Inactive":
        findings.append(
            f"{row['username']} is inactive"
        )

    role = str(row["role"]).lower()

    if any(keyword in role for keyword in [
        "admin",
        "administrator",
        "root",
        "cyberark"
    ]):
        findings.append(
            f"{row['username']} has privileged access"
        )

    if row["last_login_days"] > 90:
        findings.append(
            f"{row['username']} is dormant"
        )

print("\nIAM Findings\n")

for finding in findings:
    print("-", finding)


# AI Assessment Function
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

    report += """

Recommendations:
• Enable MFA for privileged users
• Review dormant accounts
• Remove unnecessary privileged access
• Perform quarterly access certification

=================================
"""

    return report


# Generate report
assessment = generate_assessment(findings)

print(assessment)