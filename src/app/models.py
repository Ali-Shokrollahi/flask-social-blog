from flask import current_app as app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, username, password, id=None, *args, **kwargs):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.first_name = ''
        self.last_name = ''
        self.bio = ''
        self.image = None

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_user(user_id):
        with app.app_context():
            mysql = app.extensions.get('mysql')
            conn = mysql.connection
            cur = conn.cursor()

            query = "SELECT id, email, username, password, first_name, last_name, bio, image FROM Users WHERE id = %s"
            cur.execute(query, (user_id,))
            user_data = cur.fetchone()

            if user_data:
                return User(**user_data)

        return None

    @staticmethod
    def get_user_by(identifier: str, value):
        if identifier not in ["username", "email"]: raise ValueError(
            "Invalid identifier. Must be either 'username' or 'email'.")

        with app.app_context():
            mysql = app.extensions.get('mysql')
            conn = mysql.connection
            cur = conn.cursor()

            query = f"SELECT id, email, username, password, first_name, last_name, bio, image FROM Users WHERE {identifier} = %s"

            cur.execute(query, (value,))
            user_data = cur.fetchone()

            if user_data:
                return User(**user_data)

        return None

    def check_password(self, password):
        return self.password == password

    def save_to_database(self):
        with app.app_context():
            mysql = app.extensions.get('mysql')
            # Connect to the database
            conn = mysql.connection
            cur = conn.cursor()

            # Insert or update the user data in the Users table
            query = "INSERT INTO Users (email, username, password) VALUES (%s, %s, %s) "

            values = (self.email, self.username, self.password)
            cur.execute(query, values)

            if self.id is None:
                self.id = cur.lastrowid

            # Commit the transaction
            conn.commit()

            # Close the cursor
            cur.close()

    def update_profile(self):
        with app.app_context():
            mysql = app.extensions.get('mysql')
            # Connect to the database

            conn = mysql.connection
            cur = conn.cursor()

            # Update the user's profile in the Users table
            query = "UPDATE Users SET first_name=%s, last_name=%s, bio=%s, image=%s WHERE email=%s"
            values = (self.first_name, self.last_name, self.bio, self.image, self.email)
            cur.execute(query, values)

            # Commit the transaction
            conn.commit()

            # Close the cursor
            cur.close()
