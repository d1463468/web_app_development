# 食譜收藏系統 - 路由設計文件 (API Design)

這份文件記錄了系統中所有的 Flask 路由（Routes）定義、前端請求的 HTTP 方法，以及預期的 Jinja2 網頁模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **食譜首頁** | GET | `/` | `recipes/index.html` | 顯示所有食譜，支援過濾。 |
| **食譜列表** | GET | `/recipes` | `recipes/index.html` | 首頁的別名，與 `/` 相同。 |
| **新增食譜頁面** | GET | `/recipes/new` | `recipes/form.html` | 顯示空白的新增食譜表單。 |
| **建立食譜** | POST | `/recipes` | — | 接收表單資料，建立成功後重導向至詳細頁。 |
| **食譜詳情** | GET | `/recipes/<int:recipe_id>` | `recipes/detail.html` | 根據 ID 顯示單筆食譜內容。 |
| **編輯食譜頁面** | GET | `/recipes/<int:recipe_id>/edit` | `recipes/form.html` | 顯示預填資料的編輯表單。 |
| **更新食譜** | POST | `/recipes/<int:recipe_id>/update`| — | 接收更新表單資料，更新後重導向。 |
| **刪除食譜** | POST | `/recipes/<int:recipe_id>/delete`| — | 刪除後重導向至首頁。 |
| **隨機推薦** | GET | `/recipes/random` | — | 隨機挑選食譜並重導向至詳情頁。 |
| **網址匯入預覽** | POST | `/recipes/import` | — | 接收網址，解析後重導向至 `/recipes/new` 並帶入參數。 |
| **分類管理頁面** | GET | `/categories` | `categories/index.html` | 顯示所有分類與新增表單。 |
| **建立分類** | POST | `/categories` | — | 建立新分類，重導向至管理頁面。 |
| **刪除分類** | POST | `/categories/<int:category_id>/delete`| — | 刪除指定分類，重導向至管理頁面。 |

## 2. 每個路由的詳細說明

### Recipe Routes (`/recipes`)
- **`GET /recipes`**
  - **輸入**：Query Parameters `?q=` (關鍵字), `?category_id=` (分類過濾)
  - **處理邏輯**：呼叫 `RecipeModel.get_all(search_query, category_id)`
  - **輸出**：渲染 `recipes/index.html`
- **`GET /recipes/new`**
  - **輸出**：渲染 `recipes/form.html`
- **`POST /recipes`**
  - **輸入**：表單欄位 `title`, `ingredients`, `instructions`, `image_url`, `source_url`, `notes`, `category_id`
  - **處理邏輯**：資料驗證後，呼叫 `RecipeModel.create(data)`
  - **輸出**：`redirect(url_for('recipes.detail', recipe_id=new_id))`
  - **錯誤處理**：如果標題為空，使用 `flash` 顯示錯誤並重新渲染表單。
- **`GET /recipes/<id>`**
  - **輸入**：URL 參數 `recipe_id`
  - **處理邏輯**：呼叫 `RecipeModel.get_by_id(recipe_id)`
  - **輸出**：渲染 `recipes/detail.html`
  - **錯誤處理**：找不到回傳 404
- **`POST /recipes/<id>/delete`**
  - **處理邏輯**：呼叫 `RecipeModel.delete(recipe_id)`
  - **輸出**：`redirect(url_for('recipes.index'))`

### Category Routes (`/categories`)
- **`GET /categories`**
  - **處理邏輯**：呼叫 `CategoryModel.get_all()`
  - **輸出**：渲染 `categories/index.html`
- **`POST /categories`**
  - **輸入**：表單欄位 `name`
  - **處理邏輯**：呼叫 `CategoryModel.create(name)`
  - **輸出**：`redirect(url_for('categories.index'))`
- **`POST /categories/<id>/delete`**
  - **處理邏輯**：呼叫 `CategoryModel.delete(category_id)`
  - **輸出**：`redirect(url_for('categories.index'))`

## 3. Jinja2 模板清單

所有的視圖模板將建立在 `app/templates/` 目錄中：

1. `base.html` (核心佈局版型，包含導覽列與頁尾)
2. `recipes/index.html` (繼承 `base.html`，顯示列表)
3. `recipes/detail.html` (繼承 `base.html`，顯示單筆資訊)
4. `recipes/form.html` (繼承 `base.html`，新增與編輯共用)
5. `categories/index.html` (繼承 `base.html`，分類管理頁)
