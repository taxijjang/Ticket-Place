class MovieService:
    def __init__(self, movie_dao, config):
        self.movie_dao = movie_dao
        self.config = config

    def ping(self):
        return 'NORMAL', "pong"

    def get_movie_list(self, pagination_data):
        status, data, limit = self.movie_dao.get_movie_list(pagination_data)
        pagination = {'page': pagination_data['page'], 'per_page': pagination_data['per_page'], 'limit': limit}

        return status, data, pagination

    def post_movie_list(self, movie_data):
        status, data = self.movie_dao.insert_movie(movie_data)
        return status, data

    def put_movie_list(self, modify_movie):
        status, data = self.movie_dao.update_movie(modify_movie)
        return status, data

    def get_movie_detail(self, movie_cd):
        status, data = self.movie_dao.get_movie_detail(str(movie_cd))
        return status, data

    def delete_movie_detail(self, movie_cd):
        status, data = self.movie_dao.erase_movie(str(movie_cd))
        return status, data
