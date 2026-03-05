from langchain_core.messages import HumanMessage
from graph.state import CodeReviewState
from utils.llm import llm
from config.settings import SUPPORTED_LANGUAGES

ROUTER_PROMPT = """You are a programming language detector.
Given the code snippet below, identify the programming language.

Respond with ONLY one word from this list (lowercase):
{languages}

If unsure, respond with: unknown

Code:
{code}
"""

def router_node(state: CodeReviewState) -> CodeReviewState:
    print("🔀 [Router] Detecting programming language...")
    prompt = ROUTER_PROMPT.format(
        languages=", ".join(SUPPORTED_LANGUAGES),
        code=state['raw_code'][:500]
    )
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        detected = response.content.strip().lower()
        language = detected if detected in SUPPORTED_LANGUAGES else "unknown"
        print(f"   ✅ Detected: {language.upper()}")
        return {**state, 'language': language}
    except Exception as e:
        return {**state, 'language': "unknown", 'error': str(e)}