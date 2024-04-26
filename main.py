import json
import os
from string import Template

import streamlit as st
import pandas as pd

import qianfan_client


def read_file_string(path):
    with open(path, 'r') as f:
        file_content = f.read()
        return file_content


def download_file(file_path):
    with open(file_path, "rb") as f:
        file_content = f.read()
    return file_content


def main():
    st.title("对话情感分析")
    uploaded_file = st.file_uploader("上传CSV文件", type=["csv"])

    if uploaded_file is not None:
        with open("./resource/conversation.csv", 'wb') as f:
            f.write(uploaded_file.getbuffer())
        df = pd.read_csv(uploaded_file)
        st.write(df)  # 显示

    prompt_input = st.text_area("修改Prompt")
    if st.button("保存Prompt"):
        with open('./resource/prompt.txt', 'w') as f:
            f.write(prompt_input)
        st.success("Prompt成功保存")

    if st.button("开始分析对话内容"):
        df = pd.read_csv('./resource/conversation.csv')
        if df is None:
            st.write("请先上传对话文本")
        else:
            print(df)
            # 组装文本
            template = "{}.{}\n"
            conversations = ""
            index = 0
            for sentence in df['待分析语句']:
                conversation = template.format(index, sentence)
                index = index + 1
                conversations = conversations + conversation
            print("conversations:\n", conversations)
            with open("./resource/prompt.txt", "r") as f:
                prompt_template_string = f.read()
            print("prompt:\n", prompt_template_string)
            prompt_template = Template(prompt_template_string)
            prompt = prompt_template.substitute(conversations=conversations)
            result = qianfan_client.complete(prompt)
            result = remove_first_and_last_line(result)
            print(result)
            df = parse_llm_result(result)
            df.to_csv("./resource/tag_result.csv", index=True)
            st.dataframe(df, width=800, height=1200)
            file_content = download_file("./resource/tag_result.csv")
            st.download_button(label="点击下载", data=file_content,file_name="tag_result.csv")


def parse_llm_result(result):
    tag_dict = json.loads(result)
    df = pd.read_csv('./resource/conversation.csv')
    # 添加一列 是否骂人
    for index, value in tag_dict.items():
        df.at[int(index), '标记结果'] = value
    return df


def remove_first_and_last_line(text):
    # 使用 splitlines() 方法将字符串分割成行
    lines = text.splitlines()

    # 删除第一行和最后一行
    if len(lines) > 1:
        lines = lines[1:-1]
    else:
        lines = []

    # 将剩余行重新组合成字符串
    result = '\n'.join(lines)

    return result


if __name__ == "__main__":
    os.environ["QIANFAN_ACCESS_KEY"] = "ALTAKLyd5EswPU4vMBM3eC6C8U"
    os.environ["QIANFAN_SECRET_KEY"] = "f6e9da6c27aa41f09936dc98e60d414e"
    main()
