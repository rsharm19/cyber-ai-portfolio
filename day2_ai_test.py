import requests

print("================================")
print(" Cybersecurity + AI Portfolio ")
print("================================")

question = input("Ask a cybersecurity question: ")

# Simple demo response logic
responses = {
    "what is phishing": "Phishing is a cyber attack where attackers trick users into revealing sensitive information.",
    "what is sql injection": "SQL Injection is a vulnerability where attackers manipulate database queries.",
    "what is xss": "Cross-site scripting (XSS) allows attackers to inject malicious scripts into web pages.",
    "what is mfa": "MFA adds an extra authentication layer for better security.",
    "what is saml": "SAML Security Assertion Markup Language is an XML-based open standard that facilitates"
    
}

answer = responses.get(
    question.lower(),
    "AI response not available yet. Add more intelligence later."
)

print("\nAI Security Assistant Response:")
print(answer)