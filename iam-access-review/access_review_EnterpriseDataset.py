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
# STEP 4: Read CSV File
# ====================================

df = pd.read_csv("enterprise_users.csv")

print("\n================================")
print(" IAM Access Review Analyzer ")
print("================================\n")

print(df)


# ====================================
# STEP 5: Convert CSV Data to Text
# ====================================

access_data = df.to_string(index=False)


# ====================================
# STEP 6: Create AI Prompt
# ====================================

prompt = f"""
You are a senior IAM security auditor.

Analyze the IAM dataset carefully.

Use these rules:

1. Any account containing:
   - shared
   - temp
   - test
   - admin
   should be reviewed as potentially risky.

2. Any account with:
   - risk_score above 80
   is HIGH RISK.

3. Any privileged role like:
   - Global Admin
   - Privileged Admin
   - Root Account
   - Database Admin
   should be reviewed carefully.

4. Any inactive privileged account is CRITICAL.

5. Any account without MFA enabled is a security concern.

6. Any contractor account should be reviewed for expiration risk.

7. Shared accounts are compliance risks.

Provide output in this format:

- Critical Findings
- High Risk Users
- MFA Issues
- Dormant Accounts
- Shared Account Risks
- Contractor Risks
- Recommended Remediation

IAM Dataset:

{access_data}
"""

# ====================================
# STEP 7: Call AI Model
# ====================================

try:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity IAM expert."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    findings = response.choices[0].message.content

    # ====================================
    # STEP 8: Print Findings
    # ====================================

    print("\n================================")
    print(" AI SECURITY FINDINGS ")
    print("================================\n")

    print(findings)

    # ====================================
    # STEP 9: Save Findings
    # ====================================

    with open("findings_Dataset.txt", "w") as file:
        file.write(findings)

    print("\nFindings saved to findings.txt")

except Exception as e:

    print("Error occurred:")
    print(e)