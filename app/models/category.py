from app.database import get_db_connection


class CategoryModel:
    """食譜分類的資料模型，提供 categories 資料表的 CRUD 操作。"""

    @staticmethod
    def create(data):
        """
        新增一筆分類記錄。

        Args:
            data (dict): 分類資料，必須包含 'name' 欄位。
                - name (str): 分類名稱（不可重複）。

        Returns:
            int: 新建分類的 ID。
            None: 若新增失敗則回傳 None。
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (data.get('name'),)
            )
            conn.commit()
            category_id = cursor.lastrowid
            conn.close()
            return category_id
        except Exception as e:
            print(f"[CategoryModel.create] 錯誤：{e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有分類記錄，依名稱排序。

        Returns:
            list[dict]: 所有分類記錄的列表，每筆為一個字典。
            list: 若查詢失敗則回傳空列表。
        """
        try:
            conn = get_db_connection()
            categories = conn.execute(
                "SELECT * FROM categories ORDER BY name"
            ).fetchall()
            conn.close()
            return [dict(cat) for cat in categories]
        except Exception as e:
            print(f"[CategoryModel.get_all] 錯誤：{e}")
            return []

    @staticmethod
    def get_by_id(category_id):
        """
        根據 ID 取得單筆分類記錄。

        Args:
            category_id (int): 分類的唯一識別碼。

        Returns:
            dict: 該分類的資料字典。
            None: 若找不到該分類或查詢失敗則回傳 None。
        """
        try:
            conn = get_db_connection()
            category = conn.execute(
                "SELECT * FROM categories WHERE id = ?",
                (category_id,)
            ).fetchone()
            conn.close()
            return dict(category) if category else None
        except Exception as e:
            print(f"[CategoryModel.get_by_id] 錯誤：{e}")
            return None

    @staticmethod
    def update(category_id, data):
        """
        更新一筆分類記錄。

        Args:
            category_id (int): 要更新的分類 ID。
            data (dict): 更新的資料，可包含：
                - name (str): 新的分類名稱。

        Returns:
            bool: 更新成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE categories SET name = ? WHERE id = ?",
                (data.get('name'), category_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[CategoryModel.update] 錯誤：{e}")
            return False

    @staticmethod
    def delete(category_id):
        """
        刪除一筆分類記錄。

        根據 schema 的 ON DELETE SET NULL 設定，
        刪除分類時，關聯食譜的 category_id 會自動變為 NULL。

        Args:
            category_id (int): 要刪除的分類 ID。

        Returns:
            bool: 刪除成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                "DELETE FROM categories WHERE id = ?",
                (category_id,)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[CategoryModel.delete] 錯誤：{e}")
            return False
