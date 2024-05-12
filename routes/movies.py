from flask import Blueprint, request,jsonify
from models import Movies

movie_bp = Blueprint('movies',__name__)    

@movie_bp.route('/movies',methods = ['POST','GET'])
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
    