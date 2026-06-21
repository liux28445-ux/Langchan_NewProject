import os

from openai import OpenAI

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://llm-70sfrw87l0tl2plg.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

res =client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {'role':'system', 'content':'你是一个python编程专家，并且不说废话简单回答'},
        {'role':'assistant', 'content':'好的。我是编程专家，并且话多，请问你要问什么'},
        {'role':'user', 'content':'请写一个python代码，将一个列表中的所有数字乘以2'}
    ],
    stream=True
)


# print(res.choices[0].message.content)

for c in res:
    print(
        c.choices[0].delta.content,
        end=" ",
        flush=True
    )