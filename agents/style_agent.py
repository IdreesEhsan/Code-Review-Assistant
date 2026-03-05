from langchain_core.messages import HumanMessage
from graph.state import CodeReviewState
from utils.llm import llm
from utils.helpers import extract_json_from_response

STYLE_PROMPT = """You are an expert {language} code style reviewer.
Analyze the following {language} code for style issues ONLY.

Focus on:
- Naming conventions (variables, functions, classes)
- Code formatting and indentation
- Function/method length and complexity
- Missing or poor documentation/comments
- Dead code, unused variables/imports
- Language-specific style guides (e.g. PEP8 for Python)

Return ONLY a valid JSON array. No explanation, no markdown prose.
Each item must have these exact keys:
  "severity"    : one of CRITICAL | HIGH | MEDIUM | LOW | INFO
  "category"    : "style"
  "line_hint"   : approximate location e.g. "line 5"
  "description" : what the problem is
  "suggestion"  : how to fix it

If no issues found, return: []

Code:
```{language}
{code}
```
"""

def style_node(state: CodeReviewState) -> dict:
    print("🎨 [Style Agent] Checking code style...")
    prompt = STYLE_PROMPT.format(
        language=state.get("language", "unknown"),
        code=state["raw_code"]
    )
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        issues = extract_json_from_response(response.content)
        print(f"   ✅ Found {len(issues)} style issue(s)")
        return {"style_issues": issues}   # ← only return YOUR field
    except Exception as e:
        return {"style_issues": [], "error": str(e)}