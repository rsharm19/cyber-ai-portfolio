# Updated script to add Menu Options
# Python-based AI cybersecurity assistant using Groq’s OpenAI-compatible API. 
# The application securely loads API keys from environment variables, uses prompt engineering
#  via system prompts, sends user questions to an LLM, and displays AI-generated cybersecurity guidance.
# ====================================
# STEP 1: Import Libraries
# ====================================

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
# STEP 4: Display Header
# ====================================

print("====================================")
print(" AI Cybersecurity Assistant ")
print("====================================")


# ====================================
# STEP 5: Topic Selection
# ====================================

print("\nChoose Topic:")
print("1. IAM")
print("2. Phishing")
print("3. MFA")
print("4. RBAC")
print("5. SAML")

topic = input("\nEnter topic number: ")

question = input("Ask your cybersecurity question: ")


# ====================================
# STEP 6: Topic Mapping
# ====================================

topic_map = {
    "1": "Identity and Access Management",
    "2": "Phishing attacks",
    "3": "Multi-Factor Authentication",
    "4": "Role-Based Access Control",
    "5": "SAML Authentication"
}

selected_topic = topic_map.get(topic, "Cybersecurity")


# ====================================
# STEP 7: Call AI Model
# ====================================

try:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a cybersecurity expert.

Focus especially on:
{selected_topic}

Explain concepts clearly for beginners.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    # ====================================
    # STEP 8: Print AI Response
    # ====================================

    print("\n==============================")
    print(" AI RESPONSE ")
    print("==============================\n")

    print(response.choices[0].message.content)

    # ====================================
    # STEP 9: Save Chat History
    # ====================================

    with open("chat_history.txt", "a") as file:
        file.write(f"\nQUESTION: {question}\n")
        file.write(f"RESPONSE: {response.choices[0].message.content}\n")

except Exception as e:

    # ====================================
    # STEP 10: Error Handling
    # ====================================

    print("Error occurred:")
    print(e)