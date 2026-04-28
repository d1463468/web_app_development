from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models import RecipeModel, CategoryModel

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/')
@recipes_bp.route('/recipes')
def index():
    """
    食譜首頁與列表。

    輸入：Query Parameters
        - q (str, optional): 搜尋關鍵字，比對食譜名稱與食材。
        - category_id (int, optional): 依分類 ID 篩選。

    輸出：渲染 recipes/index.html，顯示篩選後的食譜列表。
    """
    search_query = request.args.get('q', '').strip()
    category_id = request.args.get('category_id', type=int)

    recipes = RecipeModel.get_all(
        search_query=search_query if search_query else None,
        category_id=category_id
    )
    categories = CategoryModel.get_all()

    return render_template(
        'recipes/index.html',
        recipes=recipes,
        categories=categories,
        search_query=search_query,
        selected_category_id=category_id
    )


@recipes_bp.route('/recipes/new', methods=['GET'])
def new():
    """
    顯示新增食譜表單。

    輸出：渲染 recipes/form.html（空白表單），並傳入所有分類供下拉選單使用。
    """
    categories = CategoryModel.get_all()
    return render_template('recipes/form.html', categories=categories, recipe=None)


@recipes_bp.route('/recipes', methods=['POST'])
def create():
    """
    接收表單資料，建立新食譜。

    輸入：表單資料
        - title (str, 必填): 食譜名稱。
        - ingredients (str): 食材清單。
        - instructions (str): 料理步驟。
        - image_url (str): 圖片路徑。
        - source_url (str): 來源網址。
        - notes (str): 個人筆記。
        - category_id (int): 分類 ID。

    輸出：
        - 成功：重導向至該食譜詳情頁。
        - 失敗：flash 錯誤訊息並重新渲染 form.html。
    """
    title = request.form.get('title', '').strip()

    # 驗證必填欄位
    if not title:
        flash('食譜名稱為必填欄位，請輸入名稱。', 'error')
        categories = CategoryModel.get_all()
        return render_template('recipes/form.html', categories=categories, recipe=request.form)

    # 處理 category_id（空字串轉為 None）
    category_id = request.form.get('category_id', '').strip()
    category_id = int(category_id) if category_id else None

    data = {
        'title': title,
        'ingredients': request.form.get('ingredients', '').strip(),
        'instructions': request.form.get('instructions', '').strip(),
        'image_url': request.form.get('image_url', '').strip(),
        'source_url': request.form.get('source_url', '').strip(),
        'notes': request.form.get('notes', '').strip(),
        'category_id': category_id,
    }

    new_id = RecipeModel.create(data)

    if new_id:
        flash('食譜新增成功！', 'success')
        return redirect(url_for('recipes.detail', recipe_id=new_id))
    else:
        flash('食譜新增失敗，請稍後再試。', 'error')
        categories = CategoryModel.get_all()
        return render_template('recipes/form.html', categories=categories, recipe=request.form)


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    顯示單一食譜詳情。

    輸入：URL 參數 recipe_id (int)
    輸出：渲染 recipes/detail.html；找不到則回傳 404。
    """
    recipe = RecipeModel.get_by_id(recipe_id)

    if not recipe:
        abort(404)

    return render_template('recipes/detail.html', recipe=recipe)


@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET'])
def edit(recipe_id):
    """
    顯示編輯食譜表單。

    輸入：URL 參數 recipe_id (int)
    輸出：渲染 recipes/form.html，帶入該食譜既有資料；找不到則 404。
    """
    recipe = RecipeModel.get_by_id(recipe_id)

    if not recipe:
        abort(404)

    categories = CategoryModel.get_all()
    return render_template('recipes/form.html', categories=categories, recipe=recipe)


@recipes_bp.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update(recipe_id):
    """
    接收表單資料，更新食譜內容。

    輸入：URL 參數 recipe_id (int)，表單資料同 create。
    輸出：
        - 成功：重導向至該食譜詳情頁。
        - 驗證失敗：flash 錯誤並重新渲染 form.html。
    """
    title = request.form.get('title', '').strip()

    # 驗證必填欄位
    if not title:
        flash('食譜名稱為必填欄位，請輸入名稱。', 'error')
        categories = CategoryModel.get_all()
        return render_template('recipes/form.html', categories=categories, recipe=request.form)

    # 處理 category_id（空字串轉為 None）
    category_id = request.form.get('category_id', '').strip()
    category_id = int(category_id) if category_id else None

    data = {
        'title': title,
        'ingredients': request.form.get('ingredients', '').strip(),
        'instructions': request.form.get('instructions', '').strip(),
        'image_url': request.form.get('image_url', '').strip(),
        'source_url': request.form.get('source_url', '').strip(),
        'notes': request.form.get('notes', '').strip(),
        'category_id': category_id,
    }

    success = RecipeModel.update(recipe_id, data)

    if success:
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipes.detail', recipe_id=recipe_id))
    else:
        flash('食譜更新失敗，請稍後再試。', 'error')
        categories = CategoryModel.get_all()
        return render_template('recipes/form.html', categories=categories, recipe=request.form)


@recipes_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete(recipe_id):
    """
    刪除指定食譜。

    輸入：URL 參數 recipe_id (int)
    輸出：刪除成功後重導向至首頁 (/recipes)。
    """
    success = RecipeModel.delete(recipe_id)

    if success:
        flash('食譜已成功刪除。', 'success')
    else:
        flash('食譜刪除失敗，請稍後再試。', 'error')

    return redirect(url_for('recipes.index'))


@recipes_bp.route('/recipes/random', methods=['GET'])
def random_recipe():
    """
    隨機推薦一道食譜。

    輸出：從資料庫取得隨機食譜 ID，並重導向至其詳情頁；若無食譜則導回首頁。
    """
    recipe = RecipeModel.get_random()

    if recipe:
        return redirect(url_for('recipes.detail', recipe_id=recipe['id']))
    else:
        flash('目前沒有任何食譜，快來新增第一道吧！', 'info')
        return redirect(url_for('recipes.index'))


@recipes_bp.route('/recipes/import', methods=['POST'])
def import_recipe():
    """
    (Nice to have) 從外部網址解析並匯入食譜。

    輸入：表單資料 source_url (str)
    輸出：目前僅將網址帶入新增表單，未來可擴充為自動解析。
    """
    source_url = request.form.get('source_url', '').strip()

    if not source_url:
        flash('請輸入要匯入的網址。', 'error')
        return redirect(url_for('recipes.index'))

    # 目前僅將 source_url 帶入新增表單，未來可擴充網頁解析功能
    flash('已載入網址，請手動填寫其餘資訊。', 'info')
    categories = CategoryModel.get_all()
    return render_template(
        'recipes/form.html',
        categories=categories,
        recipe={'source_url': source_url}
    )
