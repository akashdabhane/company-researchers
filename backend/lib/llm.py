from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


# # 1. Define your LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0,
#     convert_system_message_to_human=True,  # ← required for Gemini
# )


# 1. Define your LLM
llm = ChatOllama(
    model="qwen3:4b",
    temperature=0,
)


