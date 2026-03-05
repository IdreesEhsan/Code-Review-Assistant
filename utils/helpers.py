import json
import re
import os
from datetime import datetime
from config.settings import REPORTS_DIR

def extract_json_from_response(text: str) -> list[dict]:
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("```").strip()
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            for v in result.values():
                if isinstance(v, list):
                    return v
    except json.JSONDecodeError:
        pass
    
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return []

def save_report(report: str, language: str) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{REPORTS_DIR}/review_{language}_{timestamp}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    return filename

def count_issues_by_severity(issues: list[dict]) -> dict:
    counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
    for issue in issues:
        sev = issue.get('severity', 'INFO').upper()
        if sev in counts:
            counts[sev] += 1
    return counts