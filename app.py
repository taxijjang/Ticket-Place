import config
from flask import Flask
from sqlalchemy import create_engine, text

from model import MovieDao
from service import MovieService
from view import create_endpoints

class Services:
    pass

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    print(database)
    ## Persistenace Layer
    movie_dao = MovieDao(database)

    ## Business Layer
    services = Services
    services.movie_service = MovieService(movie_dao, config)


    ## end point 생성
    create_endpoints(app, services)

    return app
