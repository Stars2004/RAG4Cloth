import streamlit as st

# streamlit run app_file_uploader.py

# 设置页面标题
st.title("文件更新服务")

# 创建文件上传组件
uploader_file = st.file_uploader(
    label="请上传 TXT 文件",
    type="txt",
    accept_multiple_files=False,    # 是否允许上传多个文件
)

if uploader_file is not None:
    # 提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  # 转换为 KB

    # 显示文件信息
    st.subheader(f"文件名: {file_name}")
    st.write(f"文件类型: {file_type} | 文件大小: {file_size:.2f} KB")

    # 读取文件内容
    file_content = uploader_file.getvalue().decode("utf-8")
    st.write(file_content)
