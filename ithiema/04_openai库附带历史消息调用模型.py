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
        {"role":"system","content":"你是AI助理，回答很简洁"},
        {"role":"user","content":"小明有2条宠物狗"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"小红有3只宠物猫"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"总共有几个宠物?"}
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