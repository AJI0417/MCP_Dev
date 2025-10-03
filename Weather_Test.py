# 匯入 os 模組，用於與作業系統互動，例如讀取環境變數
import os
# 匯入 requests 模組，用於發送 HTTP 請求以取得網路資料
import requests
# 匯入 csv 模組，用於讀寫 CSV (逗號分隔值) 檔案
import csv
# 從 dotenv 模組中匯入 load_dotenv 函數，用於從 .env 檔案載入環境變數
from dotenv import load_dotenv

# 執行 load_dotenv() 函數，讀取 .env 檔案並設定環境變數
load_dotenv()


# 定義一個名為 getWeather 的函數，接收一個城市名稱(city)作為參數
def getWeather(city):
    # 從環境變數中取得名為 "API_KEY" 的值，這是中央氣象署的 API 金鑰
    Weather_API_KEY = os.getenv("API_KEY")
    # 組合 API 的 URL，並將 API 金鑰作為授權參數傳入
    Weather_API_URL = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={Weather_API_KEY}"

    # 使用 requests.get() 發送 GET 請求到指定的 URL
    response = requests.get(Weather_API_URL)
    # 將伺服器回應的 JSON 格式資料轉換為 Python 的字典
    Weather_data = response.json()

    # 從資料中提取 "records" 裡的 "location" 列表，這裡面包含了所有縣市的預報資料
    locations = Weather_data["records"]["location"]

    # 遍歷所有地區的資料
    for location in locations:
        # 判斷當前地區的名稱是否與使用者輸入的城市名稱相符
        if location["locationName"] == city:
            # 如果相符，就提取該地區的 "weatherElement" (天氣因子)
            weather_elements = location["weatherElement"]

            # 建立一個空字典，用來存放天氣資訊
            weather_info = {}
            # 遍歷所有的天氣因子 (如：天氣狀況、降雨機率、溫度等)
            for element in weather_elements:
                # 取得天氣因子的名稱 (例如 "Wx", "PoP")
                element_name = element["elementName"]
                # 取得未來第三個時間點的預報資料 (通常是未來 12-24 小時)
                time_data = element["time"][2]

                # 判斷天氣因子的名稱
                if element_name == "Wx":  # "Wx" 代表天氣狀況
                    # 將天氣狀況的描述存入字典
                    weather_info["天氣狀態"] = time_data["parameter"]["parameterName"]
                elif element_name == "PoP":  # "PoP" 代表降雨機率 (Probability of Precipitation)
                    # 將降雨機率的數值加上 "%" 後存入字典
                    weather_info["降雨機率"] = (
                        time_data["parameter"]["parameterName"] + "%"
                    )
                elif element_name == "MinT":  # "MinT" 代表最低溫度 (Minimum Temperature)
                    # 將最低溫度的數值加上 "°C" 後存入字典
                    weather_info["最低溫度"] = (
                        time_data["parameter"]["parameterName"] + "°C"
                    )
                elif element_name == "MaxT":  # "MaxT" 代表最高溫度 (Maximum Temperature)
                    # 將最高溫度的數值加上 "°C" 後存入字典
                    weather_info["最高溫度"] = (
                        time_data["parameter"]["parameterName"] + "°C"
                    )
                elif element_name == "CI":  # "CI" 代表舒適度指數 (Comfort Index)
                    # 將天氣體感的描述存入字典
                    weather_info["天氣體感"] = time_data["parameter"]["parameterName"]

            # 回傳包含所有天氣資訊的字典
            return weather_info


# 定義一個名為 save_to_csv 的函數，接收天氣資訊、城市名稱和檔案名稱
def save_to_csv(weather_info, city_name, filename="weather_data.csv"):
    """將天氣資訊儲存為 CSV，若城市已存在則更新"""
    # 如果沒有天氣資訊，就印出訊息並結束函數
    if weather_info is None:
        print("沒有天氣資訊可以儲存")
        return

    # 在天氣資訊字典中加入一個 "城市" 的鍵值對
    weather_info["城市"] = city_name

    # 建立一個空列表來存放 CSV 的每一行資料
    rows = []
    # 從天氣資訊字典中取得所有的鍵，作為 CSV 的欄位名稱
    fieldnames = list(weather_info.keys())
    # 檢查檔案是否已經存在
    if os.path.exists(filename):
        # 如果檔案存在，就以讀取模式開啟
        with open(filename, mode="r", encoding="utf-8-sig", newline="") as file:
            # 使用 csv.DictReader 讀取 CSV 檔案，並將每一行轉換為字典
            reader = csv.DictReader(file)
            # 遍歷讀取器中的每一行
            for row in reader:
                # 將每一行(字典)加入到 rows 列表中
                rows.append(row)

        # 建立一個布林變數，用來追蹤是否已更新資料
        updated = False
        # 遍歷 rows 列表中的每一行資料
        for i, row in enumerate(rows):
            # 檢查該行的 "城市" 是否與目前的城市名稱相符
            if row.get("城市") == city_name:
                # 如果相符，就用新的天氣資訊更新該行
                rows[i] = weather_info
                # 將 updated 設為 True
                updated = True
                # 中斷迴圈
                break
        # 如果迴圈結束後 updated 仍然是 False，表示這是新的城市
        if not updated:
            # 將新的天氣資訊加入到 rows 列表中
            rows.append(weather_info)
    else:
        # 如果檔案不存在，就直接將天氣資訊加入到 rows 列表中
        rows.append(weather_info)

    # 以寫入模式開啟 CSV 檔案 (如果檔案不存在會自動建立)
    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        # 建立一個 csv.DictWriter 物件，用於將字典寫入 CSV
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # 寫入第一行，也就是欄位名稱
        writer.writeheader()
        # 將 rows 列表中的所有資料寫入檔案
        writer.writerows(rows)

    # 印出訊息，告知使用者檔案已儲存
    print(f"天氣資訊已儲存至 {filename}")


# 這是一個 Python 的標準寫法，確保以下的程式碼只在直接執行此檔案時才會被執行
if __name__ == "__main__":
    # 設定要查詢的城市名稱為 "臺中市"
    city_name = "臺中市"
    # 呼叫 getWeather 函數來取得天氣資訊
    weather = getWeather(city_name)
    # 在終端機印出天氣資訊
    print(weather)
    # 呼叫 save_to_csv 函數，將天氣資訊儲存到 "weather_data.csv" 檔案中
    save_to_csv(weather, city_name, "weather_data.csv")
