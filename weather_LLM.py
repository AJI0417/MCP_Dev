# -*- coding: utf-8 -*-
"""
此檔案使用 LangChain 和 RAG 技術，讓大型語言模型 (LLM) 能夠根據
`weather_data.json` 檔案中的天氣資料來回答使用者的問題。

它會執行以下操作：
1. 從 `weather_data.json` 載入天氣資料。
2. 將天氣資料轉換為 LangChain 的 Document 格式。
3. 使用 OllamaEmbeddings 建立文字向量。
4. 建立一個 FAISS 向量儲存庫作為檢索器 (Retriever)。
5. 設定一個本地 LLM (gemma3:4b) 模型。
6. 建立一個提示模板 (Prompt Template) 來引導 LLM 的回答。
7. 建立一個 RAG 檢索鏈 (Retrieval Chain)。
8. 啟動一個互動式循環，讓使用者可以輸入問題並獲得回答。
"""

import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


def create_rag_chain():
    """建立並返回一個 RAG 檢索鏈。"""
    # 1. 載入天氣資料
    try:
        with open("weather_data.json", "r", encoding="utf-8") as f:
            weather_data = json.load(f)
    except FileNotFoundError:
        print(
            "錯誤：找不到 weather_data.json 檔案。請先執行 Weather_API.py 來生成資料。"
        )
        return None

    # 2. 將資料轉換為 Document 物件
    documents = []
    for entry in weather_data:
        content = f"時間：從 {entry['startTime']} 到 {entry['endTime']}，天氣狀態：{entry['天氣狀態']}，降雨機率：{entry['降雨機率']}，最低溫度：{entry['最低溫度']}，最高溫度：{entry['最高溫度']}，天氣體感：{entry['天氣體感']}。"
        documents.append(Document(page_content=content))

    # 3. 設定嵌入模型
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 4. 建立 FAISS 向量儲存庫
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever()

    # 5. 設定 LLM 模型
    llm = Ollama(model="gemma3:4b")

    # 6. 建立提示模板
    prompt = PromptTemplate.from_template(
        """
        請根據以下天氣資料來回答問題。並且使用遊客中心廣播的口吻來回答
        提醒遊客要根據天氣情況來做應變 比如：天氣熱要多喝水預防中暑 天氣陰暗提醒攜帶雨具
        最後要加上遊客服務中心關心您的字樣來結束
        如果你在資料中找不到答案，請回答「我無法從目前的資料中找到答案」
        請只根據提供的資料使用中文(繁體) 回答，不要添加任何額外的天氣資訊。

        天氣資料：
        {context}

        問題：{input}

        回答："""
    )

    # 7. 建立文件處理鏈和檢索鏈
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain


def main():
    """主函式，啟動問答循環。"""
    rag_chain = create_rag_chain()

    if rag_chain is None:
        return

    print("（輸入 'exit' 或 'q' 來結束程式）")

    while True:
        user_input = input("\n您的問題是：")
        if user_input.lower() in ["exit", "q"]:
            break

        response = rag_chain.invoke({"input": user_input})
        print("\n模型回答：")
        print(response["answer"])


if __name__ == "__main__":
    main()
