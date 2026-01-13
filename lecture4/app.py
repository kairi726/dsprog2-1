from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import requests

app = Flask(__name__)
CORS(app)
DB_NAME = "weather.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_code TEXT,
            forecast_date TEXT,
            weather_code TEXT,
            temp_max TEXT,
            temp_min TEXT,
            pop TEXT,
            UNIQUE(area_code, forecast_date) ON CONFLICT REPLACE
        )''')
        conn.commit()

@app.route('/weather/<area_code>')
def get_weather(area_code):
    try:
        # 気象庁からデータ取得
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        res = requests.get(url).json()
        
        # 週間予報データの解析 (data[1]が週間予報)
        weekly = res[1]
        times = weekly['timeSeries'][0]['timeDefines']
        codes = weekly['timeSeries'][0]['areas'][0]['weatherCodes']
        pops = weekly['timeSeries'][0]['areas'][0]['pops']
        temps = weekly['timeSeries'][1]['areas'][0] # tempsMax, tempsMinが入っている
        
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            for i in range(len(codes)):
                date = times[i][:10] # YYYY-MM-DD形式
                pop = pops[i] if i < len(pops) else "--"
                t_max = temps['tempsMax'][i] if i < len(temps['tempsMax']) else "--"
                t_min = temps['tempsMin'][i] if i < len(temps['tempsMin']) else "--"
                
                cur.execute('''INSERT INTO forecasts (area_code, forecast_date, weather_code, temp_max, temp_min, pop)
                               VALUES (?, ?, ?, ?, ?, ?)''', (area_code, date, codes[i], t_max, t_min, pop))
            conn.commit()
            print(f"Log: {area_code} のデータをDBに保存しました")

    except Exception as e:
        print(f"Error: {e}")

    # DBから最新の予報を取得して返す
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM forecasts WHERE area_code = ? ORDER BY forecast_date ASC LIMIT 7", (area_code,))
        return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)