from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash



class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = ''
        self.last_name = ''
        self.bio = ''
        self.image = None

    def save_to_database(self):
        with app.app_context():
            mysql = app.extensions.get('mysql')
            # Connect to the database
            conn = mysql.connection
            cur = conn.cursor()

            # Insert or update the user data in the Users table
            query = "INSERT INTO Users (email, username, password) VALUES (%s, %s, %s) " \
                    "ON DUPLICATE KEY UPDATE email=VALUES(email), password=VALUES(password)"
            values = (self.email, self.username, self.password)
            cur.execute(query, values)

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
