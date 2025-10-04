# 臺中市天氣預報資料API串接

## 專案說明

這是一個 Python檔案，用於從中央氣象署的開放資料平台獲取臺中市的 36 小時天氣預報。檔案會將天氣資料（包括天氣狀態、降雨機率、溫度和體感等）處理後，儲存為一個名為 `weather_data.json` 的 JSON 檔案。

## 資料來源

本腳本使用的天氣資料來自[中央氣象署開放資料平台](https://opendata.cwa.gov.tw/)的「一般天氣預報-今明 36 小時天氣預報」API。

- **API 文件:** [F-C0032-001](https://opendata.cwa.gov.tw/dataset/forecast/F-C0032-001)

## 主要功能

- 獲取臺中市未來 36 小時內三個不同時間段的天氣預報。
- 將天氣資料（天氣狀態、降雨機率、最低/最高溫度、天氣體感）整理成結構化格式。
- 將處理後的資料儲存為 `weather_data.json` 檔案，方便後續應用。

## 系統需求

- Python 3.12或以上
- `requests` 函式庫
- `python-dotenv` 函式庫

## 安裝指南

1. **複製或下載專案**

2. **安裝所需的 Python 函式庫**

   在您的終端機或命令提示字元中執行以下指令：

   ```bash
   pip install requests python-dotenv
   ```

## 設定步驟

1. **獲取 API 金鑰**

   - 前往[中央氣象署開放資料平台](https://opendata.cwa.gov.tw/)
   - 註冊並登入會員。
   - 登入後，在會員中心可以找到您的 API 授權碼 (API KEY)。

2. **建立 `.env` 檔案**

   在專案的根目錄（與 `Weather_API.py` 相同的目錄）下，建立一個名為 `.env` 的檔案，並在其中加入您的 API 金鑰，格式如下：

   ```
   API_KEY="在這裡貼上您的API金鑰"
   ```

## 使用方法

完成設定後，直接執行 Python 檔案即可：

```bash
python Weather_API.py
```

腳本執行後，會在同一個目錄下生成 `weather_data.json` 檔案，並在終端機上印出獲取到的天氣資料。
