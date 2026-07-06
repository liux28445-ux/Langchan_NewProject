import ssl
import certifi

_old_create_default_context = ssl.create_default_context

def _patched_create_default_context(*args, **kwargs):
    kwargs.setdefault("cafile", certifi.where())
    return _old_create_default_context(*args, **kwargs)

ssl.create_default_context = _patched_create_default_context

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool


@tool(description="获取股票价格 ")
def get_price(name:str) -> str:
    return f"股票{name}的价格是1000元"
@tool(description="获取股票名称")
def get_name(name:str) -> str:
    return f"股票{name}的名称是腾讯"
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_price, get_name],
    system_prompt="你是一个股票查询助手,可以回答股票相关问题，记住请告诉我思考过程，让我知道你所思考的步骤"

)

for c in agent.stream(
        {"messages":[{"role": "user", "content": "传智教育股价多少，并介绍一下"}]},
    stream_mode="values"
):
    print(c["messages"][-1])