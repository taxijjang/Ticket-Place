import pytest
import json
import config
from app import create_app
from sqlalchemy import create_engine, text

database = create_engine(config.test_config['DB_URL'], encoding='UTF-8', max_overflow=0)


@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api


def setup_function():
    '''
        테스트를 하기 위한 초기 데이터 값 설정
    '''
    new_movie = {
        'movieCd': '1', 'movieNm': '테스트', 'movieNmEn': 'TEST', 'prdtYear': '2020', 'openDt': '20200101',
        'typeNm': '장편', 'prdtStatNm': '테스트', 'nationAlt': '테스트', 'genreAlt': '테스트', 'repNationNm': '테스트',
        'repGenreNm': '테스트'
    }

    database.execute(text("""
        INSERT INTO movies(
            movieCd, movieNm, movieNmEn, prdtYear, openDt, typeNm, 
            prdtStatNm, nationAlt, genreAlt, repNationNm, repGenreNm
        ) VALUES (
            :movieCd, :movieNm, :movieNmEn, :prdtYear, :openDt, :typeNm, 
            :prdtStatNm, :nationAlt, :genreAlt, :repNationNm, :repGenreNm
        )
    """), new_movie)

    print("new_moive")
    database.execute(text("""
        INSERT INTO directors(
            movieCd, peopleNm
        ) VALUES (
            '1', '테스트 디렉터'
        )
    """))

    database.execute(text("""
        INSERT INTO companys(
            movieCd, companyCd, companyNm
        ) VALUES (
            '1', '1', '테스트 컴패니'
        )
    """))


def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE movies"))
    database.execute(text("TRUNCATE directors"))
    database.execute(text("TRUNCATE companys"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


###### 엔드포인트 테스트 코드 작성

def test_ping(api):
    response = api.get('/ping')
    assert b'pong' in response.data


def test_movie_list(api):
    response = api.get('/movies')
    movie_list = json.loads(response.data.decode('utf-8'))

    # status 상태 확인:
    assert response.status_code == 200

    assert movie_list == {
        'movies': [
            {
                'genreAlt': '테스트', 'movieCd': '1', 'movieNm': '테스트',
                'movieNmEn': 'TEST', 'nationAlt': '테스트', 'openDt': '20200101'
            }
        ]
    }

def test_movie_detail(api):
    response = api.get('/movies/1')
    movie_data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200

    assert movie_data == {
        'data': {
            'genreAlt': '테스트', 'movieCd': '1', 'movieNm': '테스트', 'movieNmEn': 'TEST',
            'nationAlt': '테스트', 'openDt': '20200101', 'prdtStatNm': '테스트',
            'prdtYear': '2020', 'typeNm': '장편'
        }
    }
