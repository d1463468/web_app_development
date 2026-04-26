from app.database import get_db_connection

class CategoryModel:
    @staticmethod
    def create(name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        category_id = cursor.lastrowid
        conn.close()
        return category_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        categories = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
        conn.close()
        return [dict(cat) for cat in categories]

    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        category = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
        conn.close()
        return dict(category) if category else None

    @staticmethod
    def delete(category_id):
        conn = get_db_connection()
        # 當刪除分類時，根據 schema 設定 ON DELETE SET NULL，關聯的食譜 category_id 會變為 NULL
        conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        conn.close()
        return True
