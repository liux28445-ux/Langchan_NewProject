import os

from langchain_community.llms.tongyi import Tongyi
from langchain_ollama import OllamaLLM
# model1 = Tongyi(model="qwen3-max", api_key=os.getenv("DASHSCOPE_API_KEY"))
# print(model1.invoke(input='你是谁'))

model2 = OllamaLLM(model="qwen3:4b")
res = model2.invoke(input='你是谁')
print(res)