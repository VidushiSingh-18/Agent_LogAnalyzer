# 🔍 Agent_LogAnalyzer

An AI-powered Python agent that automatically analyzes system logs, identifies errors and root causes, and generates human-readable reports using LLMs (Ollama, OpenAI, or Google Gemini).

---

## 📁 Project Structure

```
Agent_LogAnalyzer/
├── data/
│   └── logs/                         # Input log files (.log)
│       └── api_access.log
├── outputs/
│   └── log_analyzer/                 # Generated reports (not committed)
│       ├── *_raw_<timestamp>.txt
│       ├── *_analysis_<timestamp>.txt
│       ├── *_analysis_<timestamp>.json
│       └── *_executive_<timestamp>.txt
├── src/
│   ├── agents/
│   │   └── log_analyzer.py           # Main log analyzer agent
│   └── core/
│       ├── __init__.py
│       ├── llm_client.py             # LLM provider abstraction
│       └── utils.py                  # File and JSON utility functions
├── .env                              # Environment config (not committed)
├── .env.example                      # Example env config
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ✨ Features

- 📄 Analyzes any system/application `.log` file
- 🔍 Identifies errors, warnings, and patterns
- 🌳 Finds root causes and affected systems
- 📊 Generates **3 structured output files** per run:
  - **Technical report** — detailed analysis for engineers
  - **JSON report** — structured data for integrations
  - **Executive summary** — plain English for non-technical stakeholders
- 🕐 All output files are **timestamped** — every run creates new files
- 🔄 Supports **multiple LLM providers** — switch with one line in `.env`

---

## 🔧 Supported LLM Providers

| Provider | Models | Notes |
|----------|--------|-------|
| **Ollama** (default) | `mistral:latest`, `llama3`, `codellama` | Free, runs locally, no API key needed |
| **OpenAI** | `gpt-4o`, `gpt-4o-mini` | Requires API key |
| **Google Gemini** | `gemini-1.5-flash`, `gemini-2.0-flash` | Requires API key |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/avni18/Agent_LogAnalyzer.git
cd Agent_LogAnalyzer
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
# Provider Options: openai | google | ollama
PROVIDER=ollama

# Model name
MODEL=mistral:latest

# API Keys (leave empty if using Ollama)
OPENAI_API_KEY=
GOOGLE_API_KEY=

# Ollama Host
OLLAMA_HOST=http://localhost:11434
```

### 5. (For Ollama only) Install and start Ollama
```bash
# Install from https://ollama.com
ollama pull mistral
ollama serve
```

---

## ▶️ Usage

### Run Log Analyzer
```bash
# Auto-picks first .log file in data/logs/
python src/agents/log_analyzer.py

# Or specify a file
python src/agents/log_analyzer.py data/logs/api_access.log
```

### Sample console output
```
📄 Analyzing: api_access.log
📏 Log size: 1640 characters
🕐 Run timestamp: 20260309_183521
🤖 Running analysis...
📝 Raw output saved: outputs/log_analyzer/api_access_raw_20260309_183521.txt
✅ Analysis complete!
📝 Technical report : outputs/log_analyzer/api_access_analysis_20260309_183521.txt
📊 JSON report      : outputs/log_analyzer/api_access_analysis_20260309_183521.json
👔 Executive summary: outputs/log_analyzer/api_access_executive_20260309_183521.txt
🗂  Raw output       : outputs/log_analyzer/api_access_raw_20260309_183521.txt
```

---

## 📤 Output Files

Every run generates 4 timestamped files in `outputs/log_analyzer/`:

| File | Description |
|------|-------------|
| `*_raw_<timestamp>.txt` | Full raw LLM response (for debugging) |
| `*_analysis_<timestamp>.txt` | Detailed technical report |
| `*_analysis_<timestamp>.json` | Structured JSON with errors, root causes, recommendations |
| `*_executive_<timestamp>.txt` | Plain English summary for non-technical readers |

### Sample JSON output
```json
{
  "summary": "Multiple authentication failures detected from suspicious IP",
  "error_count": 5,
  "critical_errors": [
    {
      "timestamp": "2026-01-04 10:24:12",
      "message": "Authentication failed",
      "severity": "high"
    }
  ],
  "root_causes": ["Brute force attack from IP 192.168.1.105"],
  "affected_systems": ["api", "auth"],
  "recommendations": ["Block IP 192.168.1.105", "Enable rate limiting"],
  "severity": "high"
}
```

---

## 📦 Dependencies

```
python-dotenv
openai
google-generativeai
ollama
pandas
```

Install all:
```bash
pip install -r requirements.txt
```

---

## 🔐 Security Notes

- Never commit your `.env` file — it is in `.gitignore`
- Store API keys in `~/.zshrc` for extra security:
```bash
export GOOGLE_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

---

## 🔄 Switching LLM Providers

Just update your `.env` — no code changes needed:

```env
# Use Ollama (free, local) recommended for development
PROVIDER=ollama
MODEL=mistral:latest

# Use OpenAI
PROVIDER=openai
MODEL=gpt-4o-mini

# Use Google Gemini
PROVIDER=google
MODEL=gemini-1.5-flash
```

---

## 👩‍💻 Author

**VidushiSingh** — [@VidushiSingh-18](https://https://github.com/VidushiSingh-18)

---

## 📄 License

This project is for educational and development purposes.

