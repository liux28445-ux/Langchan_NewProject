from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

c = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人,可以作诗"),
        MessagesPlaceholder("history"),
        ["human", "再来一首唐诗"]
    ]
)

history_data = [
    ("human", "写一首唐诗"),
    ("ai", "唐诗如下：\n\n白发三千丈，高挂云间。"),
    ("human", "写一首唐诗"),
    ("ai", "唐诗如下：\n\n白日依山尽，黄河入海流。")
]

print(c.invoke(input={"history": history_data}).to_string())