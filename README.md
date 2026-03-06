# 🔍 CodeScan — AI-Powered Code Review Assistant

> Multi-agent code review pipeline built with LangGraph + LangChain + Groq.
> Automatically detects bugs, style issues, and security vulnerabilities — then generates a fixed version of your code.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-1C3C3C?style=flat)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=flat)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-F55036?style=flat)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)

---

## 📸 Overview

CodeScan is an end-to-end multi-agent system where specialized AI agents run **in parallel** to review your code across three dimensions simultaneously:

- 🎨 **Style Agent** — naming conventions, formatting, readability, dead code
- 🐛 **Bug Agent** — logic errors, null dereferences, resource leaks, edge cases
- 🔐 **Security Agent** — OWASP Top 10, SQL injection, hardcoded secrets, weak crypto
- 🔧 **Fix Agent** — generates a refactored version of your code with all issues addressed
- 📋 **Reporter Agent** — produces a scored Markdown report (0–100)

---

## 🏗️ Architecture

```
User Input (code)
       │
       ▼
┌─────────────┐
│   ROUTER    │  ← Detects programming language
└──────┬──────┘
       │
  ┌────┴──────────────┬──────────────┐
  ▼                   ▼              ▼
┌────────┐     ┌──────────┐  ┌──────────────┐
│ STYLE  │     │   BUG    │  │   SECURITY   │  ← Parallel execution
│ AGENT  │     │  AGENT   │  │    AGENT     │
└────┬───┘     └────┬─────┘  └──────┬───────┘
     │              │               │
     └──────────────┼───────────────┘
                    │  (fan-in)
                    ▼
              ┌─────────────┐
              │  FIX AGENT  │  ← Generates refactored code
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │  REPORTER   │  ← Builds final scored report
              └─────────────┘
```

### Key LangGraph Concepts Used

| Concept           | Where Used                                     |
| ----------------- | ---------------------------------------------- |
| `StateGraph`      | Core graph with `CodeReviewState` TypedDict    |
| Parallel fan-out  | Router → Style + Bug + Security simultaneously |
| Fan-in merge      | All 3 agents → Fix (waits for all to complete) |
| `START` / `END`   | Entry and exit nodes                           |
| State propagation | Each node reads/writes shared state dict       |

---

## 📁 Project Structure

```
code_review_assistant/
│
├── api.py                      # FastAPI server (REST API + frontend serving)
├── main.py                     # CLI entry point (Typer + Rich)
├── requirements.txt
├── .env.example
│
├── static/
│   └── index.html              # Frontend UI (HTML + CSS + JS)
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Groq config, constants
│
├── graph/
│   ├── __init__.py
│   ├── state.py                # CodeReviewState TypedDict schema
│   └── review_graph.py         # LangGraph definition & compilation
│
├── agents/
│   ├── __init__.py
│   ├── router_agent.py         # Language detection node
│   ├── style_agent.py          # Style review node
│   ├── bug_agent.py            # Bug detection node
│   ├── security_agent.py       # Security scanning node
│   ├── fix_agent.py            # Code fix generation node
│   └── reporter_agent.py       # Final report generation node
│
├── utils/
│   ├── __init__.py
│   ├── llm.py                  # Shared ChatGroq instance
│   └── helpers.py              # JSON parsing, report saving
│
├── sample_codes/
│   ├── sample.py           # Test file with intentional issues
│   └── sample.js       # Test file with intentional issues
│
└── output_reports/             # Generated reports saved here (git ignored)
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/code-review-assistant.git
cd code-review-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

> Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## 🖥️ Running the Project

### Option A — Web UI (Recommended)

```bash
uvicorn api:app --reload --port 8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

### Option B — CLI

```bash
# Review a file
python main.py --file sample_codes/bad_python.py

# Review and save report
python main.py --file sample_codes/bad_python.py --save

# Interactive paste mode
python main.py
```

---

## 🤖 Agents Explained

### 🔀 Router Agent

Detects the programming language from the submitted code using the LLM.
Supports: Python, JavaScript, TypeScript, Java, C, C++, Go, Rust, Ruby, PHP.

### 🎨 Style Agent

Reviews code style against language-specific best practices.
Catches: bad naming, missing docstrings, dead code, long functions, PEP8 violations.

### 🐛 Bug Agent

Scans for logic errors and runtime risks.
Catches: division by zero, null dereferences, unreachable code, resource leaks, infinite loops.

### 🔐 Security Agent

OWASP-aware vulnerability scanner.
Catches: SQL injection, hardcoded secrets, XSS, eval/exec usage, weak hashing (MD5), insecure deserialization (pickle).

### 🔧 Fix Agent

Receives all issues from the three agents above and generates a refactored, improved version of the code with `# FIX:` comments explaining each change.

### 📋 Reporter Agent

Aggregates all findings into a structured Markdown report with an overall quality score (0–100) calculated from issue severity weights.

---

## 📊 Scoring System

| Severity    | Penalty Points |
| ----------- | -------------- |
| 🔴 CRITICAL | -25            |
| 🟠 HIGH     | -15            |
| 🟡 MEDIUM   | -7             |
| 🔵 LOW      | -2             |
| ⚪ INFO     | 0              |

| Score Range | Rating        |
| ----------- | ------------- |
| 90–100      | 🏆 Excellent  |
| 75–89       | ✅ Good       |
| 50–74       | ⚠️ Needs Work |
| 0–49        | ❌ Poor       |

---

## 🌐 API Reference

### `POST /review`

Runs the full review pipeline on submitted code.

**Request body:**

```json
{
  "code": "your code here",
  "language": "auto"
}
```

**Response:**

```json
{
  "language": "python",
  "score": 42,
  "total_issues": 13,
  "style_issues": [...],
  "bug_issues": [...],
  "security_issues": [...],
  "fix_suggestions": "...",
  "final_report": "..."
}
```

### `GET /health`

```json
{ "status": "ok", "service": "CodeScan API" }
```

---

## 🧪 Testing with Sample Files

```bash
# Python — most comprehensive test
python main.py --file sample_codes/bad_python.py --save

# JavaScript
python main.py --file sample_codes/bad_javascript.js --save
```

Expected output for `bad_python.py`:

- ~16 style issues
- ~8 bug issues
- ~9 security issues
- Score: ~20–40/100

---

## 🔧 Extending the Project

### Add a New Review Agent

1. Create `agents/performance_agent.py`
2. Add `performance_issues: list` to `graph/state.py`
3. Register in `graph/review_graph.py`:

```python
graph.add_node("performance", performance_node)
graph.add_edge("router", "performance")      # fan-out
graph.add_edge("performance", "fix")         # fan-in
```

### Switch LLM Provider

Update `utils/llm.py` to use OpenAI, Anthropic, or Ollama:

```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

# Ollama (fully local)
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3.2", temperature=0.0)
```

---

## 🛠️ Tech Stack

| Tool                                                   | Purpose                              |
| ------------------------------------------------------ | ------------------------------------ |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Multi-agent graph orchestration      |
| [LangChain](https://github.com/langchain-ai/langchain) | LLM abstraction & message handling   |
| [Groq API](https://console.groq.com)                   | Ultra-fast LLM inference (free tier) |
| LLaMA 3.3 70B                                          | Underlying language model            |
| [FastAPI](https://fastapi.tiangolo.com)                | REST API server                      |
| [Typer](https://typer.tiangolo.com)                    | CLI interface                        |
| [Rich](https://rich.readthedocs.io)                    | Beautiful terminal output            |
| Pydantic                                               | Data validation                      |

---

## 📝 Environment Variables

| Variable       | Description       | Default                   |
| -------------- | ----------------- | ------------------------- |
| `GROQ_API_KEY` | Your Groq API key | required                  |
| `GROQ_MODEL`   | Model to use      | `llama-3.3-70b-versatile` |

---

## 🙌 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) & [LangGraph](https://github.com/langchain-ai/langgraph) teams for the amazing framework
- [Groq](https://groq.com) for blazing fast free-tier inference

---

_Built with ❤️ using LangGraph + Groq_
