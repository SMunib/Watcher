from flask import Blueprint

from .auth import auth_bp
from .genres import genres_bp
from .search import search_bp
from .movies import movie_bp