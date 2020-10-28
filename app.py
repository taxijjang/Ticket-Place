from flask import Flask, request, jsonify, current_app, Response, g
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from functools import wraps


def get_movie_list():
    '''
        영화 리스트 반환
        TODO:: pagination을 이용하여 리스트 짤라서 응답하도록 하기
    :return: 영화 리스트
    '''

    movie_list = current_app.database.execute(text("""
        SELECT movieCd, movieNm, movieNmEn, openDt, genreAlt, nationAlt FROM movies ORDER BY movieCd
    """)).fetchall()

    return [{
        'movieCd': movie['movieCd'],
        'movieNm': movie['movieNm'],
        'movieNmEn': movie['movieNmEn'],
        'openDt': movie['openDt'],
        'genreAlt': movie['genreAlt'],
        'nationAlt': movie['nationAlt']
    } for movie in movie_list]


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    @app.route('/ping', methods=['GET'])
    def ping():
        return "pong", 200

    @app.route('/movies', methods=['GET'])
    def movie_list():
        return jsonify({
            'movies': get_movie_list()
        })

    return app
