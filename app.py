from flask import Flask, request, jsonify
from DatabaseManager import DatabaseManager
from flask_cors import CORS
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # You may want to restrict CORS to specific domains in production

# Initialize DatabaseManager
db_manager = DatabaseManager()
db_manager.initialize_database()

class UserManagerAPI:
    @staticmethod
    @app.route('/api/register', methods=['POST'])
    def register():
        """
        Register a new user with hashed password.
        """
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "message": "Missing username or password."}), 400

        conn = db_manager.get_connection()
        if not conn:
            return jsonify({"success": False, "message": "Database connection failed."}), 500

        try:
            cursor = conn.cursor()

            # Hash the password before storing
            hashed_password = generate_password_hash(password)

            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            return jsonify({"success": True, "message": "User registered successfully."}), 201

        except mysql.connector.IntegrityError:
            return jsonify({"success": False, "message": "Username already exists."}), 409
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    @app.route('/validate-login', methods=['POST'])
    def validate_login():
        """
        Validate user login with password comparison.
        """
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "message": "Missing username or password."}), 400

        conn = db_manager.get_connection()
        if not conn:
            return jsonify({"success": False, "message": "Database connection failed."}), 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                return jsonify({"success": True, "message": "Login successful"}), 200
            else:
                return jsonify({"success": False, "message": "Invalid username or password"}), 401
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)  # Run the server on port 9000
