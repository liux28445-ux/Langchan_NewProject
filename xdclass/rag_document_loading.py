import os.path

from langchain_community.document_loaders import PyPDFLoader

pdf_path = "/xdclass/product_manual.pdf"

if not os.path.exists(pdf_path):
    print("请将 product_manual.pdf 文件 放置到当前目录下")
    exit(1)

# 创建 PDF加载器
loader = PyPDFLoader(pdf_path)

# 执行 加载操作，pdf 每页转化为 Document对象
documents = loader.load()

print(f"加载了 {len(documents)} 页")

print("第一页前200个字符:", documents[0].page_content[:200])
