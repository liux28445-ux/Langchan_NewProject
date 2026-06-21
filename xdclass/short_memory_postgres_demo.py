import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver

# ---------- 1. 配置环境变量 ----------
if not os.getenv("DASHSCOPE_API_KEY"):
    raise ValueError("请先设置环境变量 DASHSCOPE_API_KEY")

# ---------- 2. 配置 PostgreSQL 数据库连接 ----------
DB_URI = "postgresql://postgres:postgres@42.193.143.46:5432/langchain_db"

# ---------- 3. 初始化 PostgreSQL 检查点（短记忆）----------
# 官方推荐方式：使用 with（自动关闭文件、数据库连接） 语句初始化 PostgresSaver
print("正在初始化 PostgreSQL Checkpoint（短记忆）...")
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # 自动创建 PostgreSQL 表结构
    print("PostgreSQL Checkpoint 表结构初始化成功")

    # ---------- 4. 初始化模型 ----------
    model = ChatOpenAI(
        model="qwen3.5-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.3
    )

    # ---------- 5. 创建 Agent（启用短记忆）----------
    agent = create_agent(
        model=model,
        # 定义工具
        tools=[],
        system_prompt="你是一个友好的助手",
        checkpointer=checkpointer  # 关键：启用短记忆，持久化到 PostgreSQL
    )

    # ---------- 6. 使用相同 thread_id 维持对话 ----------
    config = {"configurable": {"thread_id": "user_123_session_001"}}

    print("=== 第一轮对话 ===")
    response1 = agent.invoke(
        {"messages": [("user", "我叫老帆，喜欢编程")]},
        config=config
    )
    print("助手:", response1["messages"][-1].content)

    print("\n=== 第二轮对话（相同 thread_id，模型应记住用户）===")
    response2 = agent.invoke(
        {"messages": [("user", "我刚才说了我叫什么名字？")]},
        config=config
    )
    print("助手:", response2["messages"][-1].content)

    print("\n=== 第三轮对话 新 thread_id，模型会忘记之前的内容===")
    new_config = {"configurable": {"thread_id": "user_123_session_002"}}
    response3 = agent.invoke(
        {"messages": [("user", "我叫什么名字？")]},
        config=new_config
    )
    print("助手:", response3["messages"][-1].content)
