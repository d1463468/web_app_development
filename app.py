import os
import sqlite3
from flask import Flask
from app.routes import register_blueprints


def create_app():
    """
    應用程式工廠模式 (Application Factory)。
    初始化 Flask 應用程式並註冊所有 Blueprints。
    """
    app = Flask(
        __name__,
        template_folder='app/templates',
        static_folder='app/static'
    )

    # 從環境變數或預設值載入 SECRET_KEY
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')

    # 設定 instance 資料夾路徑
    app.config['INSTANCE_PATH'] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'instance'
    )

    # 確保 instance 資料夾存在
    os.makedirs(app.config['INSTANCE_PATH'], exist_ok=True)

    # 註冊路由 Blueprints
    register_blueprints(app)

    return app


def init_db():
    """
    初始化資料庫：讀取 database/schema.sql 並建立資料表。
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'instance', 'database.db')
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')

    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print(f'資料庫已初始化：{db_path}')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
