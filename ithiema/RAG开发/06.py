from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms.tongyi import Tongyi
from langchain_ollama.chat_models import ChatOllama
model2   = ChatOllama(model="qwen3:4b")
ex = PromptTemplate.from_template("单词:{word}, 反义词:{antonym}")

exda = [
    {"word":"大", "antonym":"小"},
    {"word":"高", "antonym":"低"},
    {"word":"黑", "antonym":"白"}
]
f = FewShotPromptTemplate(
    example_prompt=ex,
    examples = exda,
    prefix="告知我单词的反义词，我提供如下的示意",
    suffix="基于前面的示例告知我，{input}的反义词是？",
    input_variables=["input"]
)
print(f.invoke(input={"input": "大"}))
print(model2.invoke(input=f.invoke(input={"input": "大"})))