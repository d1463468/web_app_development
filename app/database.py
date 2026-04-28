import sqlite3
import os

# 預設資料庫存放路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')


def get_db_connection():
    """
    取得與 SQLite 資料庫的連線。

    Returns:
        sqlite3.Connection: 已設定 row_factory 與外鍵支援的資料庫連線物件。

    說明:
        - 使用 sqlite3.Row 作為 row_factory，讓查詢結果可以用欄位名稱取值（如 row['title']）。
        - 啟用 PRAGMA foreign_keys，確保外鍵約束生效（SQLite 預設不啟用）。
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn
