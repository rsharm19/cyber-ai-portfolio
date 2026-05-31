# ====================================
# STEP 1: Import Libraries
# ====================================

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os


# ====================================
# STEP 2: Load Environment Variables
# ====================================

load_dotenv()


# ====================================
# STEP 3: Create AI Client
# ====================================

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# ====================================
# STEP 4: Load IAM Dataset
# ====================================

df = pd.read_csv("C:\\cyber-ai-portfolio\\iam-access-review\\enterprise_users.csv")

print("\n===================================")
print(" ENTERPRISE IAM RISK DASHBOARD ")
print("===================================\n")

print(df)

# Remove hidden spaces
df.columns = df.columns.str.strip()

# Print columns for debugging
print("\nCSV Columns:")
print(df.columns.tolist())

# ====================================
# STEP 5: Risk Classification
# ====================================

def classify_risk(row):

    score = row["risk_score"]

    if score >= 90:
        return "Critical"

    elif score >= 70:
        return "High"

    elif score >= 40:
        return "Medium"

    else:
        return "Low"


df["severity"] = df.apply(classify_risk, axis=1)


# ====================================
# STEP 6: Detect Security Issues
# ====================================

issues = []

for index, row in df.iterrows():

    findings = []

    if row["status"] == "Inactive" and "Admin" in row["role"]:
        findings.append("Inactive privileged account")

    if row["MFA_enabled"] == "No":
        findings.append("MFA disabled")

    if "shared" in row["username"].lower():
        findings.append("Shared account risk")

    if "contractor" in row["account_type"].lower():
        findings.append("Contractor access review required")

    if row["risk_score"] >= 90:
        findings.append("Critical risk score")

    issues.append(", ".join(findings))

df["findings"] = issues


# ====================================
# STEP 7: Save Risk Report
# ====================================

df.to_csv("risk_report.csv", index=False)

print("\nRisk report generated: risk_report.csv")


# ====================================
# STEP 8: Convert Dataset to Text
# ====================================

access_data = df.to_string(index=False)


# ====================================
# STEP 9: AI Prompt
# ====================================

prompt = f"""
You are a senior IAM governance auditor.

Analyze the IAM dataset and provide:

1. Executive summary
2. Critical findings
3. Top risky users
4. MFA compliance concerns
5. Dormant privileged accounts
6. Shared account risks
7. Contractor risks
8. Remediation recommendations

IAM Dataset:

{access_data}
"""


# ====================================
# STEP 10: Call AI Model
# ====================================

try:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an enterprise IAM governance expert."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    ai_findings = response.choices[0].message.content


    # ====================================
    # STEP 11: Print Findings
    # ====================================

    print("\n===================================")
    print(" AI IAM SECURITY FINDINGS ")
    print("===================================\n")

    print(ai_findings)


    # ====================================
    # STEP 12: Save Findings
    # ====================================

    with open("findings_risk.txt", "w") as file:
        file.write(ai_findings)

    print("\nAI findings saved to findings.txt")

except Exception as e:

    print("Error occurred:")
    print(e)