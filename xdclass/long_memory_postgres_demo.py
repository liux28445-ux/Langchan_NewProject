import os
import uuid
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.postgres import PostgresStore
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

# ---------- 1. 配置环境变量 ----------
if not os.getenv("DASHSCOPE_API_KEY"):
    raise ValueError("请先设置环境变量 DASHSCOPE_API_KEY")

# ---------- 2. 配置 PostgreSQL 数据库连接 ----------
DB_URI = "postgresql://postgres:postgres@42.193.143.46:5432/langchain_db"

# ---------- 3. 初始化 Store（长记忆）----------
with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()  # 自动创建 PostgreSQL 表结构

    # ---------- 4. 初始化模型 ----------
    model = ChatOpenAI(
        model="qwen3.5-plus",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.3
    )


    # ---------- 5. 定义工具 ----------
    @tool
    def save_user_preference(key: str, value: str, config: RunnableConfig) -> str:
        """保存用户偏好到长期记忆"""
        user_id = config["configurable"]["user_id"]
        namespace = ("user_preferences", user_id)
        item_id = str(uuid.uuid4())
        store.put(namespace, item_id, {"key": key, "value": value})
        return f"已保存偏好 {key}={value}"


    @tool
    def get_all_user_preferences(config: RunnableConfig) -> str:
        """获取用户的所有偏好设置"""
        # 从 RunnableConfig 中获取 user_id
        user_id = config["configurable"]["user_id"]
        # 定义命名空间
        namespace = ("user_preferences", user_id)
        # 从 Store 中查询所有偏好设置
        items = store.search(namespace)
        preferences = []
        for item in items:
            key = item.value.get("key", "未知")
            value = item.value.get("value", "未知")
            preferences.append(f"{key}: {value}")
        return "\n".join(preferences) if preferences else "没有找到偏好设置"


    # ---------- 6. 创建 Agent ----------
    # 初始化 InMemorySaver（短记忆）
    checkpointer = InMemorySaver()
    agent = create_agent(
        model=model,
        # 定义工具
        tools=[save_user_preference, get_all_user_preferences],
        system_prompt="你是一个助手，可以使用工具保存和查询用户偏好。",
        checkpointer=checkpointer,  # 关键：启用短记忆，持久化到InMemorySaver
        store=store  # 关键：启用长记忆，持久化到 PostgreSQL
    )

    # ---------- 7. 测试 ----------
    user_id = "user_001"
    config = {"configurable": {"user_id": user_id, "thread_id": "session_001"}}

    print("=== 第一轮对话：保存用户偏好 ===")
    response1 = agent.invoke(
        {"messages": [("user", "我是老帆，喜欢可爱的回答，请帮我记住这个偏好。")]},
        config=config
    )
    print("助手:", response1["messages"][-1].content)

    print("\n=== 新会话（不同 thread_id）===")
    config2 = {"configurable": {"user_id": user_id, "thread_id": "session_002"}}
    response2 = agent.invoke(
        {"messages": [("user", "我是谁？我有什么偏好？")]},
        config=config2
    )
    print("助手:", response2["messages"][-1].content)
