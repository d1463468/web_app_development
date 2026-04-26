from flask import Blueprint
from .recipe_routes import recipes_bp
from .category_routes import categories_bp

def register_blueprints(app):
    """
    註冊所有的 Blueprint 到 Flask 應用程式。
    """
    app.register_blueprint(recipes_bp)
    app.register_blueprint(categories_bp, url_prefix='/categories')
