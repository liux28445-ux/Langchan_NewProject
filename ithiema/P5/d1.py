import ssl
import certifi

_old_create_default_context = ssl.create_default_context

def _patched_create_default_context(*args, **kwargs):
    kwargs.setdefault("cafile", certifi.where())
    return _old_create_default_context(*args, **kwargs)

ssl.create_default_context = _patched_create_default_context


import os

from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


@tool(description="查询天气")
def get_weather() -> str:
    return "晴天"


agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather],
    system_prompt="你是一个乐于助人的助手"
)

res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "你好，请告诉我明天的天气"}
        ]
    }
)

# print(res)
for msg in res["messages"]:
    print(type(msg).__name__,msg.content)