import streamlit as st

st.title("知识库更新服务")

uploader_file = st.file_uploader(
    "请上传知识库文件",
    type=["txt", "pdf", "docx", "pptx", "xlsx", "csv"],
    accept_multiple_files=False
)
if uploader_file is not None:
    uploader_file_name = uploader_file.name
    uploader_file_size = uploader_file.size
    uploader_file_type = uploader_file.type
    st.subheader(f"文件信息{uploader_file_name}")
    st.write(f"文件大小：{uploader_file_size}")
    st.write(f"文件类型：{uploader_file_type}")