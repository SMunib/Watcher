from flask import Blueprint, request,jsonify
from models import db,Users,Movies

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register',methods = ['POST'])
def register():
    data = request.get_json()
    new_user = Users(username = data.get('username'),email = data.get('email'))
    new_user.set_password(data.get('password'))
    
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
                    "status" : 200
                }
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
    
@auth_bp.route('/select',methods = ['GET','Post'])
def displaygenres():
    if request.method == 'Get':
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
        genres_list = request.json.get('genres')
        response = {}
        try:
            for genre in genres_list:
                movies = Movies.query.filter(Movies.Genres.contains(genre)).order_by(Movies.AvgVote.desc()).limit(3).all()
                movie_list = []
                for movie in movies:
                    movie_list.append({
                        'title':movie.Title,
                        'genres':movie.Genres,
                        'rating':movie.AvgVote
                    })
                response[genre] = movie_list
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)})

@auth_bp.route('/movies',methods = ['POST','GET'])
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

@auth_bp.route('/search',methods = ['POST'])
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
    