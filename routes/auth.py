from flask import Blueprint, request,jsonify
from models import db,Users

auth_bp = Blueprint('auth', __name__)

#register user
@auth_bp.route('/register',methods = ['POST'])
def register():
    info = request.get_json()
    new_user = Users(username = info.get('username'),email = info.get('email'))
    new_user.set_password(info.get('password'))
    
    try:
        db.session.add(new_user)
        db.session.commit()
        data = {
            "message":"User Successfully Registered!",
            "status": 200
        }
        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        error = {
            "message": str(e),
            "status": 500
        }
        return jsonify(error)

#login user
@auth_bp.route('/login', methods = ['Get','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = Users.query.filter_by(email=email).first_or_404()
            if user.check_password(password):
                data = {
                    "message" : "Login Successful",
                    "status" : 200,
                    "isFirstTime": user.isFirstTime,
                    "userid":user.id
                }
                user.isFirstTime = False
                db.session.commit()
                return jsonify(data)
            else:
                return jsonify({"message": "Invalid Username or Password", "status": 401})
        except Exception as e:
            error = {
                "message" : str(e),
                "status": 500
            }
            return jsonify(error)
    else:
        return "Hello"
