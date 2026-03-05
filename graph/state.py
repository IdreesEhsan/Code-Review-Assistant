from typing import TypedDict, Optional

class ReviewIssue(TypedDict):
    severity: str
    category: str
    line_hint: str
    description: str
    suggestion: str
    
class CodeReviewState(TypedDict):
    # Input
    raw_code: str
    language: str
    
    # Agent Outputs
    style_issues: list[ReviewIssue]
    bug_issues: list[ReviewIssue]
    security_issues: list[ReviewIssue]
    fix_suggestions: str
    
    # Final Output
    final_report: str
    
    # Control
    error: Optional[str]