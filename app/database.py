import sqlite3
import os

# 預設資料庫存放路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """
    取得與 SQLite 資料庫的連線。
    預設使用 sqlite3.Row，以便可以使用欄位名稱（如 row['title']）來存取資料。
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
