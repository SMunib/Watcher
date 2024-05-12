from flask import Flask
from flask_cors import CORS
from models import db
from routes import auth_bp,movie_bp,search_bp,genres_bp

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WatcherDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
app.register_blueprint(auth_bp,url_prefix='/auth')
app.register_blueprint(genres_bp,url_prefix='/genres')
app.register_blueprint(movie_bp,url_prefix='/movie')
app.register_blueprint(search_bp,url_prefix='/search')

db.init_app(app)
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)