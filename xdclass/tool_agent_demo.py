import os
from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# ---------- 1. 初始化 Tavily 客户端 ----------
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# tavily_client = TavilyClient(api_key='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')

# ---------- 2. 定义搜索工具 ----------f
@tool
def search_web(query: str) -> str:
    """搜索互联网获取实时信息，参数 query 是搜索关键词。当用户需要最新信息、新闻、天气、事件等时使用此工具。"""
    try:
        result = tavily_client.search(query, max_results=3)
        # 提取搜索结果中的摘要
        summaries = [item["content"] for item in result.get("results", [])]
        return "\n".join(summaries) if summaries else "未找到相关信息"
    except Exception as e:
        return f"搜索失败：{str(e)}"


# ---------- 3. 初始化模型 ----------
model = ChatOpenAI(
    model="qwen3.5-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.3
)

# ---------- 4. 创建 Agent 并绑定工具 ----------
agent = create_agent(
    model=model,
    tools=[search_web],
    system_prompt="你是一个乐于助人的助手，可以搜索互联网获取实时信息。当用户询问天气、新闻、最新事件时，请使用 search_web 工具。"
)

# ---------- 5. 测试 ----------
if __name__ == "__main__":
    print("=== 测试1：需要实时信息的问题 ===")
    response = agent.invoke(
        {"messages": [("user", "今天广州天气怎么样？请搜索后回答")]}
    )
    print("助手：", response["messages"][-1].content)

    print("\n=== 测试2：不需要搜索的问题 ===")
    response2 = agent.invoke(
        {"messages": [("user", "什么是 LangChain？请用一句话解释")]}
    )
    print("助手：", response2["messages"][-1].content)
