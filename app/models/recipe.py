from app.database import get_db_connection


class RecipeModel:
    """食譜的資料模型，提供 recipes 資料表的 CRUD 操作。"""

    @staticmethod
    def create(data):
        """
        新增一筆食譜記錄。

        Args:
            data (dict): 食譜資料，包含以下欄位：
                - title (str): 食譜名稱（必填）。
                - ingredients (str, optional): 食材清單。
                - instructions (str, optional): 料理步驟。
                - image_url (str, optional): 圖片路徑。
                - source_url (str, optional): 來源網址。
                - notes (str, optional): 個人筆記與心得。
                - category_id (int, optional): 分類 ID。

        Returns:
            int: 新建食譜的 ID。
            None: 若新增失敗則回傳 None。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO recipes (
                    title, ingredients, instructions, image_url,
                    source_url, notes, category_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                data.get('title'),
                data.get('ingredients'),
                data.get('instructions'),
                data.get('image_url'),
                data.get('source_url'),
                data.get('notes'),
                data.get('category_id'),
            )
            cursor.execute(query, values)
            conn.commit()
            recipe_id = cursor.lastrowid
            conn.close()
            return recipe_id
        except Exception as e:
            print(f"[RecipeModel.create] 錯誤：{e}")
            return None

    @staticmethod
    def get_all(search_query=None, category_id=None):
        """
        取得所有食譜記錄，支援關鍵字搜尋與分類篩選。

        Args:
            search_query (str, optional): 搜尋關鍵字，會比對食譜名稱與食材。
            category_id (int, optional): 依分類 ID 篩選。

        Returns:
            list[dict]: 食譜記錄的列表，依建立時間降冪排序。
            list: 若查詢失敗則回傳空列表。
        """
        try:
            conn = get_db_connection()
            query = """
                SELECT r.*, c.name AS category_name
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE 1=1
            """
            params = []

            if search_query:
                query += " AND (r.title LIKE ? OR r.ingredients LIKE ?)"
                params.extend([f"%{search_query}%", f"%{search_query}%"])

            if category_id:
                query += " AND r.category_id = ?"
                params.append(category_id)

            query += " ORDER BY r.created_at DESC"

            recipes = conn.execute(query, tuple(params)).fetchall()
            conn.close()
            return [dict(r) for r in recipes]
        except Exception as e:
            print(f"[RecipeModel.get_all] 錯誤：{e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """
        根據 ID 取得單筆食譜記錄，並附帶分類名稱。

        Args:
            recipe_id (int): 食譜的唯一識別碼。

        Returns:
            dict: 該食譜的資料字典，包含 category_name 欄位。
            None: 若找不到該食譜或查詢失敗則回傳 None。
        """
        try:
            conn = get_db_connection()
            query = """
                SELECT r.*, c.name AS category_name
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.id = ?
            """
            recipe = conn.execute(query, (recipe_id,)).fetchone()
            conn.close()
            return dict(recipe) if recipe else None
        except Exception as e:
            print(f"[RecipeModel.get_by_id] 錯誤：{e}")
            return None

    @staticmethod
    def update(recipe_id, data):
        """
        更新一筆食譜記錄，同時自動更新 updated_at 時間戳。

        Args:
            recipe_id (int): 要更新的食譜 ID。
            data (dict): 更新的資料，可包含以下欄位：
                - title (str): 食譜名稱。
                - ingredients (str): 食材清單。
                - instructions (str): 料理步驟。
                - image_url (str): 圖片路徑。
                - source_url (str): 來源網址。
                - notes (str): 個人筆記與心得。
                - category_id (int): 分類 ID。

        Returns:
            bool: 更新成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            query = """
                UPDATE recipes
                SET title = ?, ingredients = ?, instructions = ?,
                    image_url = ?, source_url = ?, notes = ?,
                    category_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
            values = (
                data.get('title'),
                data.get('ingredients'),
                data.get('instructions'),
                data.get('image_url'),
                data.get('source_url'),
                data.get('notes'),
                data.get('category_id'),
                recipe_id,
            )
            conn.execute(query, values)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[RecipeModel.update] 錯誤：{e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """
        刪除一筆食譜記錄。

        Args:
            recipe_id (int): 要刪除的食譜 ID。

        Returns:
            bool: 刪除成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                "DELETE FROM recipes WHERE id = ?",
                (recipe_id,)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[RecipeModel.delete] 錯誤：{e}")
            return False

    @staticmethod
    def get_random():
        """
        隨機取得一筆食譜的 ID（用於「今天吃什麼」功能）。

        Returns:
            dict: 包含隨機食譜 id 的字典。
            None: 若資料庫無食譜或查詢失敗則回傳 None。
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute(
                "SELECT id FROM recipes ORDER BY RANDOM() LIMIT 1"
            ).fetchone()
            conn.close()
            return dict(recipe) if recipe else None
        except Exception as e:
            print(f"[RecipeModel.get_random] 錯誤：{e}")
            return None
