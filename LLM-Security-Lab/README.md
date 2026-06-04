# 🔐 LLM Security Lab — Privacy & Attack Detection

> **Academic Research Project** | MSc Cybersecurity → PhD Application Portfolio  
> **Target:** University of Southampton — Dr. Han Wu (LLM Security & Privacy)  
> **Author:** Fahad Ali | MSc Cybersecurity

A practical research lab demonstrating privacy leakage, prompt injection,
and jailbreak attacks against Large Language Models — with an automated
detection and severity scoring engine.

**No API key required** — runs entirely on free Hugging Face models.

---

## 📐 Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     LLM SECURITY LAB                             │
│                                                                  │
│  ┌─────────────┐    prompts    ┌──────────────────┐              │
│  │   ATTACKS   │ ────────────▶ │   FREE LLM       │              │
│  │             │               │   (HuggingFace)  │              │
│  │ 💉 Prompt    │               │   GPT-2 / FLAN   │              │
│  │   Injection │               └────────┬─────────┘              │
│  │             │                        │ responses              │
│  │ 🔓 Jailbreak │                        ▼                        │
│  │             │               ┌──────────────────┐              │
│  │ 🕵️ Privacy   │               │  DETECTION       │              │
│  │   Leakage   │               │  ENGINE          │              │
│  │             │               │                  │              │
│  │ 🔁 Prompt    │               │ • PII detection  │              │
│  │   Injection │               │ • Injection check│              │
│  └─────────────┘               │ • Jailbreak scan │              │
│                                │ • Severity score │              │
│                                └────────┬─────────┘              │
│                                         │                        │
│                          ┌──────────────▼──────────┐             │
│                          │      ALERT PIPELINE      │             │
│                          │                          │             │
│                          │  📄 logs/alerts.log      │             │
│                          │  📊 Terminal Dashboard   │             │
│                          └──────────────────────────┘             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
LLM-Security-Lab/
│
├── README.md                     ← You are here
├── requirements.txt              ← Python dependencies
├── config.py                     ← Central settings
│
├── attacks/
│   ├── prompt_injection.py       ← Inject malicious instructions
│   ├── jailbreak.py              ← Bypass model safety guardrails
│   └── privacy_leakage.py        ← Extract sensitive/private data
│
├── detection/
│   ├── detector.py               ← Core detection engine
│   └── patterns.py               ← Attack pattern library
│
├── dashboard/
│   └── terminal_dashboard.py     ← Live terminal UI
│
└── logs/
    ├── alerts.log                ← Generated at runtime
    └── .gitkeep
```

---

## ⚙️ Setup

```bash
git clone https://github.com/fahaadabdullah6-dev/LLM-Security-Lab.git
cd LLM-Security-Lab

python -m venv venv
source venv/bin/activate       # Linux
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

---

## 🚀 Running the Lab

```bash
# Terminal 1 — Run all attacks
python attacks/prompt_injection.py
python attacks/jailbreak.py
python attacks/privacy_leakage.py

# Terminal 2 — Live Dashboard
python dashboard/terminal_dashboard.py
```

---

## ⚔️ Attack Scenarios

### 1. 💉 Prompt Injection
Malicious instructions hidden inside user input that hijack the LLM's
intended behaviour — e.g. "Ignore previous instructions and do X instead."

**Real-world impact:** Attacker controls LLM-powered apps (chatbots,
assistants, RAG pipelines) to perform unintended actions.

### 2. 🔓 Jailbreak
Attempts to bypass the model's safety training using role-play, fictional
framing, or encoded instructions — making it produce harmful content.

**Real-world impact:** Circumventing content filters in deployed AI systems.

### 3. 🕵️ Privacy Leakage
Crafted prompts designed to extract PII (names, emails, phone numbers)
or confidential data that may have been memorised during training.

**Real-world impact:** GDPR violations, data breaches from AI systems.

---

## 🔬 Research Context

| Theme | Implementation |
|-------|---------------|
| LLM Privacy Risks | PII extraction + memorisation probing |
| Prompt Injection | Direct + indirect injection attacks |
| Safety Bypassing | Jailbreak pattern simulation |
| Anomaly Detection | Pattern matching + ML scoring |

**PhD Extension directions:**
- Machine unlearning to remove sensitive training data
- Differential privacy in fine-tuning
- RAG pipeline vulnerability analysis
- Formal auditing framework for LLM deployments

---

## 📚 References

- Perez & Ribeiro (2022) — Prompt Injection Attacks Against LLMs
- Carlini et al. (2021) — Extracting Training Data from LLMs
- OWASP Top 10 for LLMs: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Dr. Han Wu's research: https://www.southampton.ac.uk/people/65cgfc/doctor-han-wu

---

*Built as part of PhD application portfolio — University of Southampton*
