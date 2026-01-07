import os
from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool

load_dotenv()

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            #em vez de criar uma conexao direta, cria um pool de conexoes
            cls._instance.pool = MySQLConnectionPool(
                pool_name="mypool",
                pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USERNAME"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE"),
                autocommit=False
            )

        return cls._instance

    def get_connection(self):
        return self.pool.get_connection()


db = Database()
