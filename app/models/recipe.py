from app.database import get_db_connection
import datetime

class RecipeModel:
    @staticmethod
    def create(data):
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
            data.get('category_id')
        )
        cursor.execute(query, values)
        conn.commit()
        recipe_id = cursor.lastrowid
        conn.close()
        return recipe_id

    @staticmethod
    def get_all(search_query=None, category_id=None):
        conn = get_db_connection()
        query = "SELECT * FROM recipes WHERE 1=1"
        params = []
        
        if search_query:
            query += " AND (title LIKE ? OR ingredients LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
            
        if category_id:
            query += " AND category_id = ?"
            params.append(category_id)
            
        query += " ORDER BY created_at DESC"
        
        recipes = conn.execute(query, tuple(params)).fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        query = """
            SELECT r.*, c.name as category_name 
            FROM recipes r 
            LEFT JOIN categories c ON r.category_id = c.id 
            WHERE r.id = ?
        """
        recipe = conn.execute(query, (recipe_id,)).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def update(recipe_id, data):
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
            recipe_id
        )
        conn.execute(query, values)
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_random():
        conn = get_db_connection()
        query = "SELECT id FROM recipes ORDER BY RANDOM() LIMIT 1"
        recipe = conn.execute(query).fetchone()
        conn.close()
        return dict(recipe) if recipe else None
