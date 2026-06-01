# Python-based AI cybersecurity assistant using Groq’s OpenAI-compatible API. 
# The application securely loads API keys from environment variables, uses prompt engineering
#  via system prompts, sends user questions to an LLM, and displays AI-generated cybersecurity guidance.

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("Grog_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("===================================")
print(" AI Cybersecurity Assistant ")
print("===================================")

question = input("Ask a cybersecurity question: ")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": """ You are a cybersecurity assistant.
            Explain cybersecurity concepts clearly for beginners.
            Focus on IAM, MFA, SSO, phishing, RBAC, SAML, and security best practices.
            """
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

print("\nAI Response:\n")
print(response.choices[0].message.content)