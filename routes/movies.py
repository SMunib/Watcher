from flask import Blueprint, request,jsonify
from models import Movies,Users,db

movie_bp = Blueprint('movies',__name__)    

@movie_bp.route('/display',methods = ['POST','GET'])
def displaymovies():
    #Category wise display of movies
    if request.method == 'POST':
        genre = request.json.get('genre')
        try:
            movies = Movies.query.filter(Movies.Genres.contains(genre)).all()
            movie_list = []
            for movie in movies:
                movie_list.append({
                    'title':movie.Title
                })
            return jsonify(movie_list)
        except Exception as e:
            return jsonify({"error":str(e)})
    else:
        #Top rated movies
        try:
            movies = Movies.query.order_by(Movies.AvgVote.desc()).limit(50).all()
            movie_list = []
            for movie in movies:
                movie_list.append({
                    'title':movie.Title,
                    'rating':movie.AvgVote
                })
            return jsonify(movie_list)
        except Exception as e:
            return jsonify({"error":str(e)})

@movie_bp.route('/watched',methods = ['POST'])
#add watched movies of user to db
def watchedMovies():
    movies = request.json.get('movies')
    userid = request.json.get('userid')
    try:
        user = Users.query.get(userid)
        if movies:
            for movie in movies:
                user.addFavMovie(movie)
            data = {
                "status":200,
                "message":"Watched Movies Stored"
            }
        else:
            data = {
                "status":201,
                "message":"No movies to store"
            }    
        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        error = {
            "status":500,
            "message":str(e)
        }
        return jsonify(error)

@movie_bp.route('/moviesbycategory',methods = ['GET'])
def findmovies():
    i = 0