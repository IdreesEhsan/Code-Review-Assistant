from langchain_core.messages import HumanMessage
from graph.state import CodeReviewState
from utils.llm import llm
from utils.helpers import extract_json_from_response

SECURITY_PROMPT = """You are an expert application security engineer (AppSec).
Analyze the following {language} code for security vulnerabilities ONLY.

Focus on:
- Hardcoded secrets, API keys, passwords, tokens
- SQL Injection, Command Injection, Path Traversal
- Cross-Site Scripting (XSS) risks
- Insecure deserialization
- Weak cryptography (MD5, SHA1 for passwords)
- Sensitive data exposure (logging passwords, PII)
- Missing input validation / sanitization
- Use of dangerous functions (eval, exec, pickle)

Return ONLY a valid JSON array. No explanation, no markdown prose.
Each item must have these exact keys:
  "severity"    : one of CRITICAL | HIGH | MEDIUM | LOW | INFO
  "category"    : "security"
  "line_hint"   : approximate location
  "description" : the security risk and potential attack vector
  "suggestion"  : exact remediation steps

If no issues found, return: []

Code:
```{language}
{code}
```
"""

def security_node(state: CodeReviewState) -> dict:
    print("🔐 [Security Agent] Scanning for vulnerabilities...")
    prompt = SECURITY_PROMPT.format(
        language=state.get("language", "unknown"),
        code=state["raw_code"]
    )
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        issues = extract_json_from_response(response.content)
        print(f"   ✅ Found {len(issues)} security issue(s)")
        return {"security_issues": issues}   # ← only return YOUR field
    except Exception as e:
        return {"security_issues": [], "error": str(e)}