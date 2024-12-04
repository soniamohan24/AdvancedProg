import mysql.connector
from mysql.connector import Error

# MySQL database configuration
DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "#dM1n#321",
    "database": "Company"
}

class DatabaseManager:
    def __init__(self):
        self.config = DATABASE_CONFIG

    def get_connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def initialize_database(self):
        """
        Create the users table if it doesn't exist.
        """
        conn = self.get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
                """)
                conn.commit()
            finally:
                cursor.close()
                conn.close()
