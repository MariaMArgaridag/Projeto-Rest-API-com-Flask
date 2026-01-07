import mysql.connector

class AttackTypeRepository:
    def __init__(self, db):
        self.db = db

    def create(self, type: str):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "INSERT INTO Attack_Types (type) VALUES (%s)",
                (type,)
            )

            conn.commit()

            return {
                "id": cursor.lastrowid,
                "type": type
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
            cursor.execute("SELECT * FROM Attack_Types")
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
                "SELECT * FROM Attack_Types WHERE id = %s",
                (id,)
            )
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def update(self, id: int, type: str):
        conn = self.db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "UPDATE Attack_Types SET type = %s WHERE id = %s",
                (type, id)
            )

            if cursor.rowcount == 0:
                conn.rollback()
                return None

            conn.commit()

            return {
                "id": id,
                "type": type
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
                "DELETE FROM Attack_Types WHERE id = %s",
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