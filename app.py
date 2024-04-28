from flask import Flask,redirect,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

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
    
@app.route('/register')
def register():
    data = request.get_json()
    new_user = Users(username = data.get('username'),password = data.get('password'),email = data.get('email'))
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return 'User successfully registered', 201 
    except Exception as e:
        return str(e), 500
    
if __name__ == '__main__':
    app.run(debug=True)