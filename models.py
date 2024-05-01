from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False, unique = True)
    email = db.Column(db.String(200), unique = True, nullable = True)
    password = db.Column(db.String(200), nullable = False)
    isFirstTime = db.Column(db.Boolean, default = True)
    
    def __repr__(self):
        return f"User('{self.username},'{self.email}')"
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    def checkFirstTime(self):
        self.isFirstTime = False
class Movies(db.Model):
    MovieID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.Text, nullable=False)
    Tagline = db.Column(db.Text)
    Synopsis = db.Column(db.Text)
    Genres = db.Column(db.Text)
    AdultFilm = db.Column(db.Boolean)
    Language = db.Column(db.Text)
    ReleaseDate = db.Column(db.Text)
    RunTime = db.Column(db.Integer)
    Cast = db.Column(db.Text)
    Director = db.Column(db.Text)
    Keywords = db.Column(db.Text)
    ProductionCompanies = db.Column(db.Text)
    ProductionCountries = db.Column(db.Text)
    Budget = db.Column(db.Integer)
    Revenue = db.Column(db.Integer)
    PosterLink = db.Column(db.Text)
    AvgVote = db.Column(db.REAL)
    VoteCount = db.Column(db.Integer)
    