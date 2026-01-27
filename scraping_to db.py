

import sqlite3

# 1. データベースのファイル名を指定（実行するとこの名前のファイルが生成されます）
db_name = "job_data.db"

def create_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # テーブル作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        salary_min INTEGER,
        education_required TEXT,
        has_license INTEGER
    )
    ''')
    conn.commit()
    conn.close()
    print(f"データベース '{db_name}' を作成・接続しました。")

# 実行
if __name__ == "__main__":
    create_db()


def save_job(title, salary, education, license_flag):
    # 1. データベースに接続
    conn = sqlite3.connect("job_data.db")
    cursor = conn.cursor()
    
    # 2. データを書き込む（SQL文）

    sql = "INSERT INTO jobs (title, salary_min, education_required, has_license) VALUES (?, ?, ?, ?)"
    data = (title, salary, education, license_flag)
    
    cursor.execute(sql, data)
    

    conn.commit()
    conn.close()
    print(f"✅ DBに保存しました: {title}")

    # テスト：自分の手入力データでDBに保存してみる
if __name__ == "__main__":
    # まずテーブルを作る
    create_db()
    
    # 練習用のデータを保存してみる
    print("テストデータを保存します.")
    save_job("テストエンジニア（大卒・資格あり）", 350000, "大卒", 1)
    save_job("テストエンジニア（高卒・資格なし）", 250000, "不問", 0)
    
    print("\n--- データベースの中身を確認します ---")
    # 保存したデータを取り出して表示
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()