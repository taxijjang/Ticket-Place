from flask import Flask, request, current_app, Response
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from functools import wraps

import json
from response import Response


def content_type(f):
    @wraps(f)
    def decorate_function(*args, **kwargs):
        response = Response()
        if request.method in ['PUT', 'POST']:
            content_type = request.headers.get('Content-Type')
            if str(content_type) != 'application/json':
                return response(status='NOT_ACCEPTABLE', data='None')

        return f(*args, **kwargs)

    return decorate_function


def get_movie_list():
    '''
        영화 리스트 반환
        TODO:: pagination을 이용하여 리스트 짤라서 응답하도록 하기
        TODO:: 예외처리 작업
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
        TODO:: 예외처리 작업
        :return: 특정 영화 데이터
    '''

    try:
        movie_data = current_app.database.execute(text("""
            SELECT movieCd, movieNm, movieNmEn, prdtYear, openDt, typeNm, prdtStatNm, nationAlt, genreAlt \
            FROM movies WHERE movieCd = :movie_cd
        """), {'movie_cd': movie_cd}).fetchone()

        diretors_data = current_app.database.execute(text("""
            SELECT d.id, d.movieCd, d.peopleNm FROM directors AS d 
            LEFT JOIN movies AS m ON d.movieCd = :movieCd WHERE d.movieCd = m.movieCd
        """), {'movieCd': movie_data['movieCd']}).fetchall()

        directors = [{'id': director[0], 'name': director[2]} for director in diretors_data]

        companys_data = current_app.database.execute(text("""
            SELECT c.id, c.movieCd, c.companyNm FROM companys AS c 
            LEFT JOIN movies AS m ON c.movieCd = :movieCd WHERE c.movieCd = m.movieCd
        """), {'movieCd': movie_data['movieCd']}).fetchall()

        companys = [{'id': company[0], 'name': company[2]} for company in companys_data]

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

        return 'NORMAL', data

    except Exception as ex:
        return 'NOT_FOUND', 'None'


def insert_movie(movie_data):
    '''
        특정 영화등록
        TODO:: 예외처리 작업
    '''
    try:
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

        return 'CREATE', movie_data

    except Exception as ex:
        ## DB CONFLICT
        if ex.code == 'gkpj':
            return 'CONFLICT', 'None'
        return 'NOT_FOUND', 'None'


def update_movie(movie_data):
    '''
        특정 영화 데이터 변경
        :param movie_data: 변경할 영화 데이터
    '''
    try:
        current_app.database.execute(text("""
            UPDATE movies SET movieNm = :movieNm, movieNmEn = :movieNmEn, 
            prdtYear = :prdtYear, openDt = :openDt, typeNm = :typeNm, 
            prdtStatNm = :prdtStatNm, nationAlt = :nationAlt, genreAlt = :genreAlt
            WHERE movieCd = :movieCd LIMIT 1
        """), movie_data).rowcount

        if len(movie_data['directors']) > 0:
            for director in movie_data['directors']:
                current_app.database.execute(text("""
                    UPDATE directors SET peopleNm = :peopleNm WHERE id = :id AND movieCd = :movieCd LIMIT 1
                """), {'movieCd': movie_data['movieCd'], 'id': director['id'],
                       'peopleNm': director['peopleNm']}).rowcount

        if len(movie_data['companys']) > 0:
            for company in movie_data['companys']:
                current_app.database.execute(text("""
                    UPDATE companys SET companyNm = :companyNm WHERE id = :id AND movieCd = :movieCd LIMIT 1
                """), {'movieCd': movie_data['movieCd'], 'id': company['id'], 'companyNm': company['companyNm']})

        return 'NORMAL', movie_data

    except Exception as ex:
        return ex, 'None'


def erase_movie(movie_cd):
    '''
        특정 영화 제거
        TODO:: 예외처리 작업
        :param movie_cd: 영화 code

    '''

    try:
        current_app.database.execute(text("""
            DELETE FROM movies WHERE movieCd = :movieCd
        """), {'movieCd': movie_cd})

        return 'NORMAL', movie_cd
    except Exception as ex:
        return ex, 'None'


def create_app(test_config=None):
    app = Flask(__name__)
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
        return response(status="NORMAL", data=data)

    @app.route('/movies', methods=['GET', 'POST', 'PUT'])
    @content_type
    def movie_list():

        if request.method == 'GET':
            data = {
                'movies': get_movie_list()
            }

            return response(status='NORMAL', data=data)

        elif request.method == 'POST':
            new_movie = request.json
            status, data = insert_movie(new_movie)

            return response(status=status, data=data)


        elif request.method == 'PUT':
            modify_movie = request.json
            status, data = update_movie(modify_movie)

            return response(status=status, data=data)

    @app.route('/movies/<int:movie_cd>', methods=['GET', 'DELETE'])
    def movie_detail(movie_cd):
        if request.method == 'GET':
            status, data = get_movie_detail(str(movie_cd))
            return response(status=status, data=data)

        elif request.method == 'DELETE':
            status, data = erase_movie(str(movie_cd))
            return response(status=status, data=data)

    @app.errorhandler(405)
    def error_handler(error):
        return response(status='METHOD_NOT_ALLOWED', data='None')

    return app
