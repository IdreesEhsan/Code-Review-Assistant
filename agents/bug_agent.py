from langchain_core.messages import HumanMessage
from graph.state import CodeReviewState
from utils.llm import llm
from utils.helpers import extract_json_from_response

BUG_PROMPT = """You are an expert {language} bug detection engineer.
Analyze the following {language} code for bugs and logical errors ONLY.

Focus on:
- Logic errors and incorrect conditions
- Off-by-one errors, infinite loops
- Null/None/undefined dereference risks
- Unhandled exceptions and error cases
- Incorrect data type usage
- Resource leaks (unclosed files, connections)
- Race conditions or concurrency bugs

Return ONLY a valid JSON array. No explanation, no markdown prose.
Each item must have these exact keys:
  "severity"    : one of CRITICAL | HIGH | MEDIUM | LOW | INFO
  "category"    : "bug"
  "line_hint"   : approximate location
  "description" : what the bug is and why it's a problem
  "suggestion"  : concrete fix with example if possible

If no bugs found, return: []

Code:
```{language}
{code}
```
"""

def bug_node(state: CodeReviewState) -> dict:
    print("🐛 [Bug Agent] Scanning for bugs...")
    prompt = BUG_PROMPT.format(
        language=state.get("language", "unknown"),
        code=state["raw_code"]
    )
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        issues = extract_json_from_response(response.content)
        print(f"   ✅ Found {len(issues)} bug(s)")
        return {"bug_issues": issues}   # ← only return YOUR field
    except Exception as e:
        return {"bug_issues": [], "error": str(e)}