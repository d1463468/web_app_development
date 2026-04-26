from flask import Flask
from app.routes import register_blueprints

def create_app():
    """
    應用程式工廠模式 (Application Factory)。
    初始化 Flask 應用程式並註冊所有 Blueprints。
    """
    app = Flask(__name__)
    app.secret_key = 'super-secret-key-for-development'
    
    # 註冊路由 Blueprints
    register_blueprints(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
