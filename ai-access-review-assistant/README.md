# AI-Style Access Review Assistant

## Overview

AI-Style Access Review Assistant is a Python and Streamlit-based cybersecurity application that automates Identity and Access Management (IAM) access review analysis. The solution evaluates user access data, identifies governance and security risks, and generates AI-style security assessments with actionable remediation recommendations.

---

## Business Problem

Access review and certification activities are often manual, time-consuming, and prone to oversight.

Security and IAM teams must regularly identify:

* Privileged accounts
* MFA compliance gaps
* Dormant accounts
* Inactive users
* High-risk access patterns

This project automates the review process and provides security-focused recommendations to support governance and compliance initiatives.

---

## Solution Workflow

```text
Upload Access Review CSV
        │
        ▼
Analyze User Access Data
        │
        ▼
Detect IAM Findings
        │
        ▼
Assess Risk Level
        │
        ▼
Generate AI Security Assessment
        │
        ▼
Produce Recommendations & Report
```

---

## Features

* ✅ CSV Upload Support
* ✅ IAM Findings Detection
* ✅ Privileged Account Identification
* ✅ MFA Compliance Analysis
* ✅ Dormant Account Detection
* ✅ Inactive Account Detection
* ✅ Dynamic Risk Assessment
* ✅ AI-Style Security Recommendations
* ✅ Downloadable Security Report

---

## Screenshots

### Upload Access Review Data

![Upload Screen](cyber-ai-portfolio\ai-access-review-assistant\screenshots\Upload Access Review Data.png)

### IAM Findings

![IAM Findings](cyber-ai-portfolio\ai-access-review-assistant\screenshots\IAM Findings.png)

### AI Security Assessment

![AI Security Assessment](cyber-ai-portfolio\ai-access-review-assistant\screenshots\GenerateAIAssessmentResults.png)

### Downloadable Report

![Downloadable Report](cyber-ai-portfolio\ai-access-review-assistant\screenshots\Downloadable Report.png)

---

## Technology Stack

| Technology      | Purpose                                                               |
| --------------- | --------------------------------------------------------------------- |
| Python          | Core programming language used for IAM analysis and report generation |
| Streamlit       | Interactive web application and user interface                        |
| Pandas          | CSV processing and access review analysis                             |
| GitHub          | Version control and portfolio hosting                                 |
| Streamlit Cloud | Application deployment and demonstration                              |

---

## Key IAM Concepts Demonstrated

* Access Reviews
* Access Certification
* Identity Governance
* Risk-Based Analysis
* MFA Compliance Monitoring
* Privileged Access Review
* User Lifecycle Monitoring

---

## Sample Use Cases

* Quarterly Access Certification Reviews
* Internal Security Assessments
* IAM Governance Reporting
* Compliance Validation Activities
* Privileged Access Reviews

---

## Installation

```bash
git clone <repository-url>

cd ai-access-review-assistant

pip install -r requirements.txt

streamlit run app.py
```

---

## Future Enhancements

* PDF assessment report export
* Enhanced role-based risk scoring
* Support for SailPoint and Saviynt access review reports
* Automated risk trend analysis

---

## Project Outcome

The solution enables IAM and security teams to quickly identify risky accounts, evaluate access review findings, and generate governance-focused recommendations through an intuitive and automated workflow.
