from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import RecipeModel, CategoryModel

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/')
@recipes_bp.route('/recipes')
def index():
    """
    食譜首頁與列表。
    輸入：Query Parameters `?q=` (關鍵字), `?category_id=` (分類過濾)
    輸出：渲染 recipes/index.html，顯示篩選後的食譜列表。
    """
    pass

@recipes_bp.route('/recipes/new', methods=['GET'])
def new():
    """
    顯示新增食譜表單。
    輸出：渲染 recipes/form.html (空白表單)。
    """
    pass

@recipes_bp.route('/recipes', methods=['POST'])
def create():
    """
    接收表單資料，建立新食譜。
    輸入：表單資料 (title, ingredients, instructions, etc.)
    輸出：成功後重導向至該食譜詳情頁；失敗則 flash 錯誤並重新渲染 form.html。
    """
    pass

@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    顯示單一食譜詳情。
    輸入：URL 參數 recipe_id
    輸出：渲染 recipes/detail.html；找不到則回傳 404。
    """
    pass

@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET'])
def edit(recipe_id):
    """
    顯示編輯食譜表單。
    輸入：URL 參數 recipe_id
    輸出：取得該食譜既有資料，渲染 recipes/form.html (帶入資料)；找不到則 404。
    """
    pass

@recipes_bp.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update(recipe_id):
    """
    接收表單資料，更新食譜內容。
    輸入：URL 參數 recipe_id, 表單資料
    輸出：成功後重導向至該食譜詳情頁。
    """
    pass

@recipes_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete(recipe_id):
    """
    刪除指定食譜。
    輸入：URL 參數 recipe_id
    輸出：刪除成功後重導向至首頁 (/recipes)。
    """
    pass

@recipes_bp.route('/recipes/random', methods=['GET'])
def random_recipe():
    """
    隨機推薦一道食譜。
    輸出：從資料庫取得隨機食譜 ID，並重導向至其詳情頁；若無食譜則導回首頁。
    """
    pass

@recipes_bp.route('/recipes/import', methods=['POST'])
def import_recipe():
    """
    (Nice to have) 從外部網址解析並匯入食譜。
    輸入：表單資料 (source_url)
    輸出：解析成功後重導向至 /recipes/new 並帶入解析結果；或存為草稿。
    """
    pass
