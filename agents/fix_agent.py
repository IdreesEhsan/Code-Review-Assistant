from langchain_core.messages import HumanMessage
from graph.state import CodeReviewState
from utils.llm import llm

FIX_PROMPT = """You are a senior {language} software engineer performing a code fix.

You have been given the original code and a list of issues found by review agents.
Fix ALL the issues listed below.

ISSUES FOUND:
{issues_summary}

ORIGINAL CODE:
```{language}
{code}
```

Instructions:
- Fix all CRITICAL and HIGH severity issues first
- Add inline comments explaining key fixes (prefix with # FIX:)
- Keep the original logic/intent intact
- Return ONLY the improved code block

Return format:
```{language}
<your fixed code here>
```
"""

def _format_issues(state: CodeReviewState) -> str:
    all_issues = (
        state.get("style_issues", []) +
        state.get("bug_issues", []) +
        state.get("security_issues", [])
    )
    if not all_issues:
        return "No issues found."

    lines = []
    for i, issue in enumerate(all_issues, 1):
        lines.append(
            f"{i}. [{issue.get('severity','?')}] [{issue.get('category','?').upper()}] "
            f"@ {issue.get('line_hint','?')}\n"
            f"   Problem: {issue.get('description','')}\n"
            f"   Fix: {issue.get('suggestion','')}"
        )
    return "\n\n".join(lines)

def fix_node(state: CodeReviewState) -> CodeReviewState:
    print("🔧 [Fix Agent] Generating improved code...")
    prompt = FIX_PROMPT.format(
        language=state.get("language", "unknown"),
        issues_summary=_format_issues(state),
        code=state["raw_code"]
    )
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        print("   ✅ Fixed code generated")
        return {**state, "fix_suggestions": response.content.strip()}
    except Exception as e:
        return {**state, "fix_suggestions": "Could not generate fix.", "error": str(e)}