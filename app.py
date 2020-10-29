from flask import Flask, request, current_app, Response
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from functools import wraps

import json
from response import Response


def get_movie_list():
    '''
        영화 리스트 반환
        TODO:: pagination을 이용하여 리스트 짤라서 응답하도록 하기
        TODO:: response format 설정
        :return: 영화 리스트
    '''

    movie_list = current_app.database.execute(text("""
        SELECT movieCd, movieNm, movieNmEn, openDt, genreAlt, nationAlt FROM movies ORDER BY movieCd
    """)).fetchall()

    data = [{
        'movieCd': movie['movieCd'],
        'movieNm': movie['movieNm'],
        'movieNmEn': movie['movieNmEn'],
        'openDt': movie['openDt'],
        'genreAlt': movie['genreAlt'],
        'nationAlt': movie['nationAlt']
    } for movie in movie_list]

    return data


def get_movie_detail(movie_cd):
    '''
        특정 영화 검색
        TODO:: response format 설정
        :return: 특정 영화 데이터
    '''

    movie_data = current_app.database.execute(text("""
        SELECT movieCd, movieNm, movieNmEn, prdtYear, openDt, typeNm, prdtStatNm, nationAlt, genreAlt \
        FROM movies WHERE movieCd = :movie_cd
    """), {'movie_cd': movie_cd}).fetchone()

    diretors_data = current_app.database.execute(text("""
        SELECT d.id, d.movieCd, d.peopleNm FROM directors AS d 
        LEFT JOIN movies AS m ON d.movieCd = :movieCd WHERE d.movieCd = m.movieCd
    """), {'movieCd': movie_data['movieCd']}).fetchall()

    directors = [director[2] for director in diretors_data]

    companys_data = current_app.database.execute(text("""
        SELECT c.id, c.movieCd, c.companyNm FROM companys AS c 
        LEFT JOIN movies AS m ON c.movieCd = :movieCd WHERE c.movieCd = m.movieCd
    """), {'movieCd': movie_data['movieCd']}).fetchall()

    companys = [company[2] for company in companys_data]

    data = {
        'movieCd': movie_data['movieCd'],
        'movieNm': movie_data['movieNm'],
        'movieNmEn': movie_data['movieNmEn'],
        'prdtYear': movie_data['prdtYear'],
        'openDt': movie_data['openDt'],
        'typeNm': movie_data['typeNm'],
        'prdtStatNm': movie_data['prdtStatNm'],
        'nationAlt': movie_data['nationAlt'],
        'genreAlt': movie_data['genreAlt'],
        'directors': directors,
        'companys': companys,
    }

    return data


def insert_movie(movie_data):
    '''
        특정 영화등록
    '''
    current_app.database.execute(text("""
        INSERT INTO movies (
            movieCd, movieNm, movieNmEn, prdtYear, openDt, typeNm, prdtStatNm, nationAlt, genreAlt
        ) VALUES(
            :movieCd, :movieNm, :movieNmEn, :prdtYear, :openDt, :typeNm, :prdtStatNm, :nationAlt, :genreAlt
        )
    """), movie_data).rowcount

    if len(movie_data['directors']) > 0:
        for director in movie_data['directors']:
            current_app.database.execute(text("""
                INSERT INTO directors(
                    movieCd, peopleNm
                ) VALUES (
                    :movieCd, :peopleNm
                )
            """), {'movieCd': movie_data['movieCd'], 'peopleNm': director}).rowcount

    if len(movie_data['companys']) > 0:
        for company in movie_data['companys']:
            current_app.database.execute(text("""
                INSERT INTO companys(
                    movieCd, companyNm
                ) VALUES (
                    :movieCd, :companyNm
                )
            """), {'movieCd': movie_data['movieCd'], 'companyNm': company}).rowcount

    return True


def create_app(test_config=None):
    app = Flask(__name__)
    app.run(debug=True)
    response = Response()
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    @app.route('/ping', methods=['GET'])
    def ping():
        data = "pong"
        return response(status="NORMAL", message='NORMAL', data=data)

    @app.route('/movies', methods=['GET'])
    def movie_list():
        data = {
            'movies': get_movie_list()
        }

        return response(status='NORMAL', message='NORMAL', data=data)

    @app.route('/movies/<int:movie_cd>', methods=['GET'])
    def movie_detail(movie_cd):
        data = get_movie_detail(str(movie_cd))
        return response(status='NORMAL', message='NORMAL', data=data)

    @app.route('/movies', methods=['POST'])
    def movie_post():
        new_movie = request.json
        insert_movie(new_movie)

        return response(status='NORMAL', message='NORMAL', data='')

    return app
