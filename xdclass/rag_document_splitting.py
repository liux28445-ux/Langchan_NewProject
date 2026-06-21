import os.path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = "product_manual.pdf"

if not os.path.exists(pdf_path):
    print("请将 product_manual.pdf 文件 放置到当前目录下")
    exit(1)

# 创建 PDF加载器
loader = PyPDFLoader(pdf_path)

# 执行 加载操作，pdf 每页转化为 Document对象
documents = loader.load()

# 切分文档
# 文档切分器
splitter = RecursiveCharacterTextSplitter(
    # 每块最多500个字符
    chunk_size=500,
    # 快之间的重叠字符，避免语义断裂
    chunk_overlap=50,
    # 分隔符优先级列表，按照顺序尝试切分，优先在语义边界处切分
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
)

chunks = splitter.split_documents(documents)

print(f"切分为 {len(chunks)} 个文本块")

print("第一个文本块的内容:", chunks[0].page_content[:200])
