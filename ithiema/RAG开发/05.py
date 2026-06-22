import os

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage


# model  = ChatTongyi(model="qwen3-max", api_key=os.getenv("DASHSCOPE_API_KEY"))
model2   = ChatOllama(model="qwen3:4b")
message = [
    HumanMessage(content="写一首唐诗")
]

res  = model2.stream(input= message)

for c in res:
    print(c.content,end=" ",flush=True)