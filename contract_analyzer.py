# contract_analyzer.py
# The "brain" of ContractLens. Sahil imports these functions into the Streamlit UI.

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# Load API key once when this file is imported
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_pdf_text(pdf_path: str) -> str:
    """Read a PDF and return all the text inside it as one string."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def analyze_contract(contract_text: str) -> dict:
    """
    Send a contract to Gemini and get back a structured risk analysis.
    Returns a dict with: risk_score, risk_level, summary, risks, negotiation_suggestions.
    """
    model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0.2,
    },
)

    prompt = f"""You are a contract risk analyzer. Analyze the contract below and return ONLY a valid JSON object with this exact structure:

{{
  "risk_score": <integer 1-10>,
  "risk_level": "<Low | Medium | High>",
  "summary": "<2-3 sentence plain English summary>",
  "risks": [
    {{
      "title": "<short title>",
      "severity": "<Low | Medium | High>",
      "explanation": "<1-2 sentence explanation>",
      "clause_excerpt": "<short quote from contract>"
    }}
  ],
  "negotiation_suggestions": [
    {{
      "issue": "<short issue title>",
      "suggestion": "<concrete suggested change>"
    }}
  ]
}}

Look for: auto-renewal, unlimited liability, vague IP terms, one-sided termination, indefinite confidentiality, hidden fees, broad indemnification.

Contract:
{contract_text}
"""
    response = model.generate_content(prompt)
    return json.loads(response.text)


def chat_with_contract(contract_text: str, question: str, history: list = None) -> tuple:
    """
    Ask a follow-up question about the contract.
    Returns (answer, updated_history). Sahil keeps passing history back in for multi-turn chat.
    """
    history = history or []
    history_text = "\n".join(f"Q: {q}\nA: {a}" for q, a in history)

    prompt = f"""You are a friendly legal assistant. Answer the user's question about the contract in plain English. Be concise and specific. If the contract doesn't address the question, say so honestly.

CONTRACT:
{contract_text}

PREVIOUS CONVERSATION:
{history_text}

NEW QUESTION:
{question}
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    answer = response.text
    history.append((question, answer))
    return answer, history


# ---- Demo mode: run this file directly to test all three functions ----
if __name__ == "__main__":
    # Quick local test of all three functions
    contract = extract_pdf_text("sample.pdf")
    analysis = analyze_contract(contract)

    print(f"\nRisk Score: {analysis['risk_score']}/10 ({analysis['risk_level']})")
    print(f"\nSummary: {analysis['summary']}\n")
    print("Top risks:")
    for i, risk in enumerate(analysis['risks'], 1):
        print(f"  {i}. [{risk['severity']}] {risk['title']}")

    print("\nChat mode (type 'quit' to exit):")
    history = []
    while True:
        question = input("> ").strip()
        if question.lower() in ("quit", "exit", ""):
            break
        answer, history = chat_with_contract(contract, question, history)
        print(f"\n{answer}\n")