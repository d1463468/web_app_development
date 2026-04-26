from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import CategoryModel

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def index():
    """
    顯示所有分類列表與新增分類的表單。
    輸出：渲染 categories/index.html，包含分類清單與新增欄位。
    """
    pass

@categories_bp.route('/', methods=['POST'])
def create():
    """
    建立新分類。
    輸入：表單資料 (name)
    輸出：建立成功後重導向回分類管理頁面 (categories.index)。
    """
    pass

@categories_bp.route('/<int:category_id>/delete', methods=['POST'])
def delete(category_id):
    """
    刪除指定分類。
    輸入：URL 參數 category_id
    輸出：刪除成功後重導向回分類管理頁面 (categories.index)。
    """
    pass
