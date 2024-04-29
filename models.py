from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False, unique = True)
    email = db.Column(db.String(200), unique = True, nullable = True)
    password = db.Column(db.String(200), nullable = False)
    
    def __repr__(self):
        return f"User('{self.username},'{self.email}')"
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password,password)