from flask import Flask, request, current_app, Response
from sqlalchemy import text


class MovieDao:
    def __init__(self, database):
        self.db = database

    def get_movie_list(self, pagination):
        '''
            영화 리스트 반환
            TODO:: pagination을 이용하여 리스트 짤라서 응답하도록 하기
            TODO:: 예외처리 작업
            :return: 영화 리스트
        '''

        try:
            page = pagination['page']
            per_page = pagination['per_page']

            print("############")
            print(page, per_page)

            movie_list = self.db.execute(text("""
                SELECT movieCd, movieNm, movieNmEn, openDt, genreAlt, nationAlt FROM movies ORDER BY movieCd LIMIT :page,:per_page
            """), {'page': (per_page * (page - 1)), 'per_page': per_page}).fetchall()

            print(movie_list)
            data = [{
                'movieCd': movie['movieCd'],
                'movieNm': movie['movieNm'],
                'movieNmEn': movie['movieNmEn'],
                'openDt': movie['openDt'],
                'genreAlt': movie['genreAlt'],
                'nationAlt': movie['nationAlt']
            } for movie in movie_list]

            limit = self.db.execute(text("""
                SELECT COUNT(1) FROM movies
            """))

            print("@@@@@@@@@@@@@@@@@@")
            print(page, per_page, limit)
            return 'NORMAL', data, limit // per_page

        except Exception as ex:
            return 'NOT_FOUND', 'None', 0

    def get_movie_detail(self, movie_cd):
        '''
            특정 영화 검색
            TODO:: 예외처리 작업
            :return: 특정 영화 데이터
        '''

        try:
            movie_data = self.db.execute(text("""
                SELECT movieCd, movieNm, movieNmEn, prdtYear, openDt, typeNm, prdtStatNm, nationAlt, genreAlt \
                FROM movies WHERE movieCd = :movie_cd
            """), {'movie_cd': movie_cd}).fetchone()

            diretors_data = self.db.execute(text("""
                SELECT d.id, d.movieCd, d.peopleNm FROM directors AS d 
                LEFT JOIN movies AS m ON d.movieCd = :movieCd WHERE d.movieCd = m.movieCd
            """), {'movieCd': movie_data['movieCd']}).fetchall()

            directors = [{'id': director[0], 'name': director[2]} for director in diretors_data]

            companys_data = self.db.execute(text("""
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

    def insert_movie(self, new_movie_data):
        '''
            특정 영화등록
        '''
        try:
            self.db.execute(text("""
                INSERT INTO movies (
                    movieCd, movieNm, movieNmEn, prdtYear, openDt, typeNm, prdtStatNm, nationAlt, genreAlt
                ) VALUES(
                    :movieCd, :movieNm, :movieNmEn, :prdtYear, :openDt, :typeNm, :prdtStatNm, :nationAlt, :genreAlt
                )
            """), new_movie_data).rowcount

            if len(new_movie_data['directors']) > 0:
                for director in new_movie_data['directors']:
                    self.db.execute(text("""
                        INSERT INTO directors(
                            movieCd, peopleNm
                        ) VALUES (
                            :movieCd, :peopleNm
                        )
                    """), {'movieCd': new_movie_data['movieCd'], 'peopleNm': director}).rowcount

            if len(new_movie_data['companys']) > 0:
                for company in new_movie_data['companys']:
                    self.db.execute(text("""
                        INSERT INTO companys(
                            movieCd, companyNm
                        ) VALUES (
                            :movieCd, :companyNm
                        )
                    """), {'movieCd': new_movie_data['movieCd'], 'companyNm': company}).rowcount

            return 'CREATE', new_movie_data

        except Exception as ex:
            ## DB CONFLICT
            if ex.code == 'gkpj':
                return 'CONFLICT', 'None'
            return 'NOT_FOUND', 'None'

    def update_movie(self, movie_data):
        '''
            특정 영화 데이터 변경
            :param movie_data: 변경할 영화 데이터
        '''
        try:
            self.db.execute(text("""
                UPDATE movies SET movieNm = :movieNm, movieNmEn = :movieNmEn, 
                prdtYear = :prdtYear, openDt = :openDt, typeNm = :typeNm, 
                prdtStatNm = :prdtStatNm, nationAlt = :nationAlt, genreAlt = :genreAlt
                WHERE movieCd = :movieCd LIMIT 1
            """), movie_data).rowcount

            if len(movie_data['directors']) > 0:
                for director in movie_data['directors']:
                    self.db.execute(text("""
                        UPDATE directors SET peopleNm = :peopleNm WHERE id = :id AND movieCd = :movieCd LIMIT 1
                    """), {'movieCd': movie_data['movieCd'], 'id': director['id'],
                           'peopleNm': director['peopleNm']}).rowcount

            if len(movie_data['companys']) > 0:
                for company in movie_data['companys']:
                    self.db.execute(text("""
                        UPDATE companys SET companyNm = :companyNm WHERE id = :id AND movieCd = :movieCd LIMIT 1
                    """), {'movieCd': movie_data['movieCd'], 'id': company['id'], 'companyNm': company['companyNm']})

            _, modify_movie_data = self.get_movie_detail(movie_data['movieCd'])
            return 'NORMAL', modify_movie_data

        except Exception as ex:
            return ex, 'None'

    def erase_movie(self, movie_cd):
        '''
            특정 영화 제거
            :param movie_cd: 영화 code

        '''

        try:
            self.db.execute(text("""
                DELETE FROM movies WHERE movieCd = :movieCd
            """), {'movieCd': movie_cd})

            return 'NORMAL', movie_cd
        except Exception as ex:
            return ex, 'None'
