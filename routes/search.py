from flask import Blueprint, request,jsonify
from models import Movies

search_bp = Blueprint('search',__name__)

@search_bp.route('/search',methods = ['POST'])
def searchmovie():
    #searching movie by name
    title = request.json.get('title')
    try:
        movies = Movies.query.filter(Movies.Title.like(f"%{title}%")).limit(5).all()
        movie_list = []
        for movie in movies:
            movie_list.append({
                'title':movie.Title,
                'rating':movie.AvgVote
            })
        return jsonify(movie_list)
    except Exception as e:
        return jsonify({"error": str(e)})
