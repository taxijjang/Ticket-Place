import config
from flask import Flask
from sqlalchemy import create_engine, text

from model import MovieDao
from service import MovieService
from view import create_endpoints

class Services:
    pass

def create_app(test_config=None):
    '''
        총 3개의 layer로 이루어 짐
        레이어드 패턴 (layered pattern)을 이용하였습니다.
        model, service, view
    '''
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)

    ## model
    movie_dao = MovieDao(database)

    ## service
    services = Services
    services.movie_service = MovieService(movie_dao, config)

    ## end point 생성
    create_endpoints(app, services)

    return app
