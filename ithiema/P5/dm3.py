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


@tool(description="获取体重 ")
def get_price() -> int:
    return 40
@tool(description="获取身高")
def get_name() -> int:
    return 172
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_price, get_name],
    system_prompt="你是一个BMI计算助手，记住请告诉我思考过程，让我知道你所思考的步骤"

)

for c in agent.stream(
        {"messages":[{"role": "user", "content": "计算我的BMI"}]},
    stream_mode="values"
):
    print(c["messages"][-1])