import os
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


# ---------- 1. 定义 Pydantic 模型 ----------
class Resume(BaseModel):
    """简历信息模型"""
    name: str = Field(description="候选人姓名")
    phone: Optional[str] = Field(default=None, description="手机号码，格式为11位数字")
    email: Optional[str] = Field(default=None, description="电子邮箱地址")
    skills: List[str] = Field(default_factory=list, description="掌握的技能关键词列表")


# ---------- 2. 初始化模型（使用阿里云百炼 qwen3.5-plus）----------
model = ChatOpenAI(
    model="qwen3.5-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.1  # 降低随机性，提高输出稳定性
)

# ---------- 3. 绑定结构化输出 ----------
# 系统提示词
system_prompt = "你是一个简历信息提取助手，请从用户提供的简历文本中提取信息，并以 JSON 格式返回。使用以下英文键名：name（姓名）、phone（电话）、email（邮箱）、skills（技能列表）。"

# 绑定结构化输出
structured_model = model.with_structured_output(Resume, include_raw=True)

# ---------- 4. 测试数据 ----------
resume_text = """
姓名：张三
电话：13812345678
邮箱：zhangsan@example.com
掌握 Python、Java、SQL，有三年后端开发经验。
"""

# ---------- 5. 调用并获取结构化结果 ----------
# 添加系统提示到输入文本
input_with_prompt = system_prompt + "\n\n" + resume_text
result = structured_model.invoke(input_with_prompt)

# ---------- 6. 打印结果 ----------
print("=== 结构化输出结果 ===")
if result.get("parsed"):
    parsed_result = result["parsed"]
    print(f"姓名：{parsed_result.name}")
    print(f"电话：{parsed_result.phone}")
    print(f"邮箱：{parsed_result.email}")
    print(f"技能：{', '.join(parsed_result.skills)}")
    print(f"\n原始 Pydantic 对象：{parsed_result}")
else:
    print("解析失败！")
    print(f"原始输出：{result.get('raw')}")
    print(f"错误信息：{result.get('parsing_error')}")
