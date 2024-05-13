from flask import Blueprint, request,jsonify
from models import UserRating,db
from datetime import datetime

rating_bp = Blueprint('rating', __name__)

@rating_bp.route('/setrating',methods = ['POST'])
def setRating():
    rating = request.json.get('rating')
    userid = request.json.get('userid')
    movieid = request.json.get('movieid')
    print(userid)
    new_rating = UserRating(userid = userid, movieid = movieid, whenWatched = datetime.now(), rating = rating)
    try:
        db.session.add(new_rating)
        db.session.commit()
        data = {
            "status":200,
            "message":"Rating Set"
        }
        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        data = {
            "status":500,
            "message":str(e)
        }
        return jsonify(data)
    