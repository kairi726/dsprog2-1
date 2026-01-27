import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 1. CSV読み込み
try:
    df = pd.read_csv("data.csv", encoding="shift_jis")
except:
    df = pd.read_csv("data.csv", encoding="utf-8")

# 2. DB保存
db = sqlite3.connect("job_data.db")
df.to_sql("jobs", db, if_exists="replace", index=False)

# 3. SQL実行
query = 'SELECT "licence(資格)", AVG("salary(給与・年収)") as avg_price FROM jobs GROUP BY "licence(資格)"'
result = pd.read_sql_query(query, db)

# 4. グラフ表示
print("--- Analysis Result ---")
print(result)

# 棒グラフの設定
plt.bar(result['licence(資格)'].astype(str), result['avg_price'], color=['gray', 'blue'])
plt.xlabel('License (0:No, 1:Yes)')
plt.ylabel('Average Salary')
plt.title('Analysis of Salary by License')

plt.show()
db.close()