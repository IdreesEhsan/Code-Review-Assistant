from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY, GROQ_MODEL

def  get_llm(temperature: float=0.1) -> ChatGroq:
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=temperature,
        api_key=GROQ_API_KEY
    )
    
llm = get_llm()