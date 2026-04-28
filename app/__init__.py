# app 套件初始化檔案

import sys
import os

# 將 init_db 從根目錄的 app.py 匯出，以便 `from app import init_db` 可用
# 注意：因為 app/ 套件與 app.py 同名，需要特殊處理
_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def init_db():
    """
    初始化資料庫：讀取 database/schema.sql 並建立資料表。
    此函式為方便匯入而在此定義，實際邏輯亦可從 app.py 呼叫。
    """
    import sqlite3
    db_path = os.path.join(_base_dir, 'instance', 'database.db')
    schema_path = os.path.join(_base_dir, 'database', 'schema.sql')

    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print(f'資料庫已初始化：{db_path}')
