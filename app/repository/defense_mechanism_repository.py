import mysql.connector

class DefenseMechanismRepository:
    def __init__(self, db):
        self.db = db

    def create(self, mechanism: str):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "INSERT INTO Defense_Mechanisms (mechanism) VALUES (%s)",
                (mechanism,)
            )

            conn.commit()

            return {
                "id": cursor.lastrowid,
                "mechanism": mechanism
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
            cursor.execute("SELECT * FROM Defense_Mechanisms")
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
                "SELECT * FROM Defense_Mechanisms WHERE id = %s",
                (id,)
            )
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    def update(self, id: int, mechanism: str):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "UPDATE Defense_Mechanisms SET mechanism = %s WHERE id = %s",
                (mechanism, id)
            )

            if cursor.rowcount == 0:
                conn.rollback()
                return None
            
            conn.commit()

            return {
                "id": id,
                "mechanism": mechanism
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
                "DELETE FROM Defense_Mechanisms WHERE id = %s",
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
