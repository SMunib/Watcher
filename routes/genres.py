from flask import Blueprint, request,jsonify
from models import db,Movies,Users

genres_bp = Blueprint('genres',__name__)

@genres_bp.route('/select',methods = ['GET','Post'])
#Display all unique genres for selection
def displaygenres():
    if request.method == 'GET':
        try:
            genres = db.session.query(Movies.Genres).all()
            unique_genres = set()
            for genres_str in genres:
                genres = genres_str[0].split(', ')
                unique_genres.update(genres)
            unique_genres.discard('') 
            return jsonify(list(unique_genres))
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        #Send three best movies according to the genres selected by the user
        genres_list = request.json.get('genres')
        # response = {}
        try:
            movie_list = []
            for genre in genres_list:
                movies = Movies.query.filter(Movies.Genres.contains(genre)).order_by(Movies.AvgVote.desc()).limit(3).all()
            data ={
                    "status":200,
                    "movies":movies
                }    
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

@genres_bp.route('/store',methods = ['POST'])
#Store the favorite genres of the user in the database
def storeGenres():
    genres_list = request.json.get('genres')
    userid = request.json.get('userid')
    
    try:
        user = Users.query.get(userid)
        if genres_list:
            for genre in genres_list:
                #print(genre)
                user.addFavouriteGenre(genre)
            data = {
                "status":200,
                "message":"Favorite Genres Stored"
            }
        else:
            data = {
                "status":201,
                "message":"No Genres to Store"
            }
        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        error = {
            "status":500,
            "message":str(e)
        }
        return jsonify(error)