from flask import request
from functools import wraps

from lib.response import Response


def content_type_check(f):
    @wraps(f)
    def decorate_function(*args, **kwargs):
        response = Response()
        if request.method in ['PUT', 'POST']:
            content_type = request.headers.get('Content-Type')
            if str(content_type) != 'application/json':
                return response(status='NOT_ACCEPTABLE', data='None')

        return f(*args, **kwargs)

    return decorate_function


def create_endpoints(app, services):
    response = Response()
    movie_service = services.movie_service

    @app.route('/ping', methods=['GET'])
    def ping():
        status, data = movie_service.ping()
        return response(status=status, data=data)

    @app.route('/movies', methods=['GET', 'POST', 'PUT'])
    @content_type_check
    def movie_list():
        if request.method == 'GET':
            pagination_data = {
                'page': int(request.args.get('page', 1)),
                'per_page': int(request.args.get('per_page', 20)),
            }

            status, data, pagination = movie_service.get_movie_list(pagination_data)
            return response(status=status, data=data, pagination=pagination)

        elif request.method == 'POST':
            new_movie_data = request.json
            status, data = movie_service.post_movie_list(new_movie_data)
            return response(status=status, data=data)

        elif request.method == 'PUT':
            modify_movie_data = request.json
            status, data = movie_service.put_movie_list(modify_movie_data)
            return response(status=status, data=data)

    @app.route('/movies/<int:movie_cd>', methods=['GET', 'DELETE'])
    @content_type_check
    def movie_detail(movie_cd):
        if request.method == 'GET':
            status, data = movie_service.get_movie_detail(movie_cd)
            return response(status=status, data=data)

        elif request.method == 'DELETE':
            status, data = movie_service.delete_movie_detail(movie_cd)
            return response(status=status, data=data)

    @app.errorhandler(405)
    def error_handler(error):
        return response(status='METHOD_NOT_ALLOWED', data='None')
