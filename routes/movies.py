from flask import Blueprint, request,jsonify
from models import Movies,Users,db
from sqlalchemy.sql.expression import func

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
                    'id':movie.MovieID,
                    'poster_path':movie.PosterLink
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

@movie_bp.route('/moviesbycategory',methods = ['POST'])
# Displays movies according to the category sent
def findmovies():
    genre = request.json.get('genre')
    try:
        movie_list = []
        movies = Movies.query.filter(Movies.Genres.contains(genre)).order_by(func.random()).limit(16).all()
        for movie in movies:
            movie_list.append({
                'id':movie.MovieID,
                'poster_path':movie.PosterLink
            })
        data = {
            "status":200,
            "movies":movie_list
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"status":500,"message":str(e)})
    
@movie_bp.route('/movieinfo',methods = ['POST'])
def sendInfo():
    id = request.json.get('MovieId')
    try:
        movie = Movies.query.get(id)
        info = {
            'title':movie.Title,
            'synopsis':movie.Synopsis,
            'runtime': movie.RunTime,
            'genres':movie.Genres,
            'rating':movie.AvgVote,
            'release':movie.ReleaseDate
        }
        return jsonify(info)
    except Exception as e:
        error = {
            "status":500,
            "message":str(e)
        }
        return jsonify(error)    

@movie_bp.route('/addtolist',methods = ['POST'])
#add to myList using movieId and userId as input
def addToFav():
    movieId = request.json.get('movieid')
    userId = request.json.get('userid')
    try:
        user = Users.query.get(userId)
        user.addtolist(movieId)
        data ={
            "status":200,
            "message":"Added to List"
        }
        return jsonify(data)
    except Exception as e:
        error = {
            "status":500,
            "message":str(e)
        }
        return jsonify(error)
    