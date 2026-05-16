# 📄 ContractLens

> AI-powered contract risk analyzer. Upload any contract PDF and get instant risk scores, plain-English summaries, and negotiation strategy — powered by Google Gemini 2.5 Flash.

![Built with Gemini](https://img.shields.io/badge/Built%20with-Gemini%202.5%20Flash-F59E0B?style=flat-square)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)

---

## 🚨 The Problem

Companies sign hundreds of contracts every year — NDAs, vendor agreements, SaaS subscriptions, partnership deals. Lawyers charge **$300+/hour** to review them, and small businesses often sign blindly, getting burned by hidden auto-renewals, unlimited liability clauses, vague IP terms, and one-sided termination rights.

## ✨ The Solution

ContractLens analyzes any contract in 30 seconds using Gemini 2.5 Flash's long-context reasoning. Upload a PDF and instantly see:

- **Risk score (1–10)** with color-coded severity and animated gauge
- **Identified risks** with severity ratings, plain-English explanations, and direct clause excerpts
- **Summary** in plain English — what you're actually agreeing to
- **Negotiation suggestions** with concrete replacement language for each problematic clause
- **Chat-with-your-contract** — ask follow-up questions and get specific answers grounded in the document

## 🎯 Why It Matters

| Metric | Value |
|---|---|
| Average lawyer cost per contract review | $1,200+ |
| Time saved per contract review | 2–4 hours |
| Target market | Every business that signs contracts |
| Business model | Per-document analysis or subscription |

## 🧠 How It Works

1. User uploads a contract PDF
2. PyPDF2 extracts the full text
3. Gemini 2.5 Flash analyzes risks via structured JSON output
4. Dashboard renders risk gauge, severity donut, expandable risk cards, and negotiation tips
5. User can ask follow-up questions through the built-in chat

## 🛠️ Tech Stack

- **AI Model:** Google Gemini 2.5 Flash via `google-generativeai`
- **PDF Parsing:** PyPDF2
- **UI Framework:** Streamlit with custom CSS (dark mode, glassmorphism, Fraunces + Manrope + JetBrains Mono typography)
- **Data Visualization:** Plotly (risk gauge, severity donut)
- **Language:** Python 3.11
- **Deployment:** Streamlit Cloud

## 🚀 Live Demo

🔗 **[contractlens.streamlit.app](https://contractlens.streamlit.app)** *(URL will be updated after deployment)*

## 💻 Run Locally

```bash
# Clone the repo
git clone https://github.com/syedshahdanish/contractlens.git
cd contractlens

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
# Create a .env file in the root with this single line:
# GEMINI_API_KEY=your_key_here
# (Get a free key at https://aistudio.google.com)

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## 📸 Screenshots

*Full dashboard screenshots coming soon — risk gauge, severity breakdown, expandable risk cards, and conversational chat interface.*

## 🏆 Hackathon

Built for **Transforming Enterprise Through AI** — hosted by [lablab.ai](https://lablab.ai) in partnership with TechEx North America, May 11–19, 2026.

- **Track:** AI Agents with Google AI Studio
- **Powered by:** Google DeepMind & Google AI Studio
- **Prize Pool:** $10,000

## 👥 Team

- **[@syedshahdanish](https://github.com/syedshahdanish)** — Full-stack development: Gemini AI integration, PDF analysis pipeline, Streamlit dashboard, UI/UX design, and deployment
- **[@sahilkingrani](https://github.com/sahilkingrani)** — Presentation materials, slide deck, and demo video

## 📄 License

MIT — feel free to fork, modify, and build on top of this.

---

*ContractLens. See every risk before you sign.*