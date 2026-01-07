import mysql.connector

class TargetIndustryRepository:
    def __init__(self, db):
        self.db = db

    def create(self, industry: str):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "INSERT INTO Target_Industries (industry) VALUES (%s)",
                (industry,)
            )

            conn.commit()

            return {
                "id": cursor.lastrowid,
                "industry": industry
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def list(self):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Target_Industries")
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    def get_by_id(self, id: int):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Target_Industries WHERE id = %s",
                (id,)
            )
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    def update(self, id: int, industry: str):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "UPDATE Target_Industries SET industry = %s WHERE id = %s",
                (industry, id)
            )

            if cursor.rowcount == 0:
                conn.rollback()
                return None
            
            conn.commit()

            return {
                "id": id,
                "industry": industry
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    def delete(self, id: int):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "DELETE FROM Target_Industries WHERE id = %s",
                (id,)
            )

            if cursor.rowcount == 0:
                conn.rollback()
                return False

            conn.commit()
            return True

        except mysql.connector.Error as err:
            conn.rollback()
            if err.errno == 1451:
                return "FK"
            raise
        finally:
            if cursor:
                cursor.close()
            conn.close()
