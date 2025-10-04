# 天氣預報及問答系統

## 專案說明

這是一個包含兩個 Python 的專案：

1.  **`Weather_API.py`**: 從中央氣象署 (CWA) 的開放資料平台獲取臺中市的 36 小時天氣預報，並將資料儲存為 `weather_data.json`。
2.  **`Weather_LLM.py`**: 使用大型語言模型 (LLM) 和 `weather_data.json` 檔案，讓您可以透過問答的方式查詢天氣資訊。

---

## 第一部分：`Weather_API.py` - 天氣資料擷取

### 功能

- 獲取臺中市未來 36 小時內三個不同時間段的天氣預報。
- 整理天氣資料（天氣狀態、降雨機率、最低/最高溫度、天氣體感）。
- 將處理後的資料儲存為 `weather_data.json` 檔案。

### 資料來源

- **API:** [中央氣象署開放資料平台 - 一般天氣預報-今明 36 小時天氣預報](https://opendata.cwa.gov.tw/dataset/forecast/F-C0032-001)

### 系統需求

- Python 3.12或以上
- `requests`
- `python-dotenv`

### 設定與使用

1.  **獲取 API 金鑰**:
    - 前往[中央氣象署開放資料平台](https://opendata.cwa.gov.tw/)註冊並登入。
    - 在會員中心找到您的 API 授權碼 (API KEY)。

2.  **建立 `.env` 檔案**:
    - 在專案根目錄下建立一個 `.env` 檔案。
    - 加入您的 API 金鑰：
      ```
      API_KEY="在這裡貼上您的API金鑰"
      ```

3.  **安裝套件**:
    ```bash
    pip install requests python-dotenv
    ```

4.  **執行腳本**:
    ```bash
    python Weather_API.py
    ```
    執行後會生成 `weather_data.json` 檔案。

---

## 第二部分：`Weather_LLM.py` - 天氣問答系統

### 功能

- 讀取 `weather_data.json` 的天氣資料。
- 使用 LangChain 和 FAISS 建立一個 RAG (Retrieval-Augmented Generation) 系統。
- 讓使用者可以用自然語言提問，並由大型語言模型 (LLM) 根據天氣資料回答。

### 系統需求

- Python 3.12或以上
- `langchain`
- `langchain-community`
- `faiss-cpu`
- `ollama` (或其他您選擇的 LLM 服務)
- `nomic-embed-text` (或其他您選擇的向量模型)
- `gemma3:4b` (或其他您選擇的其他LLM模型)

### 設定與使用

1.  **確保 `weather_data.json` 已存在**:
    - 請先執行 `Weather_API.py` 來生成天氣資料檔案。

2.  **安裝套件**:
    ```bash
    pip install langchain langchain-community faiss-cpu ollama
    ```

3.  **設定大型語言模型 (LLM)**:
    - 此腳本預設使用 `Ollama` 來運行本地的 `gemma3:4b` 模型和 `nomic-embed-text` 向量模型。
    - 請確保您已經安裝並運行了 Ollama，並且模型已經下載。
    - 如果您想使用不同的模型，請修改 `Weather_LLM.py` 中的 `Ollama` 和 `OllamaEmbeddings` 設定。

4.  **執行腳本**:
    ```bash
    python Weather_LLM.py
    ```
    執行後，您可以開始在終端機中輸入關於天氣的問題。
