import pytest
import json
import config

from view.app import create_app
from sqlalchemy import create_engine, text

from lib.response import Response

database = create_engine(config.test_config['DB_URL'], encoding='UTF-8', max_overflow=0)
print(config.test_config['DB_URL'])

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
    response = Response()
    api_response = api.get('/ping')
    payload = json.loads(api_response.data.decode('utf-8'))

    assert api_response.status_code == 200
    assert payload == response(status='NORMAL', data=payload['data'], unit_test=True)


def test_movie_list(api):
    response = Response()
    api_response = api.get('/movies')
    payload = json.loads(api_response.data.decode('utf-8'))

    # status 상태 확인:
    assert api_response.status_code == 200

    data = {
        'movies': [{
            'movieCd': '1', 'genreAlt': '테스트', 'movieNm': '테스트',
            'movieNmEn': 'TEST', 'nationAlt': '테스트', 'openDt': '20200101'
        }]
    }
    assert payload == response(status='NORMAL', data=data, unit_test=True)


def test_movie_detail(api):
    response = Response()
    api_response = api.get('/movies/1')
    payload = json.loads(api_response.data.decode('utf-8'))

    assert api_response.status_code == 200

    data = {
        'companys': [{'id': 1, 'name': '테스트 컴패니'}], 'directors': [{'id': 1, 'name': '테스트 디렉터'}], 'genreAlt': '테스트',
        'movieCd': '1', 'movieNm': '테스트', 'movieNmEn': 'TEST', 'nationAlt': '테스트',
        'openDt': '20200101', 'prdtStatNm': '테스트', 'prdtYear': '2020', 'typeNm': '장편'
    }

    assert payload == response(status='NORMAL', data=data, unit_test=True)

    ## 없는 데이터 조회 했을때
    api_response = api.get('/movies/2')
    payload = json.loads(api_response.data.decode('utf-8'))

    assert api_response.status_code == 200
    assert payload == response(status='NOT_FOUND', data='None', unit_test=True)


def test_movie_insert(api):
    response = Response()
    request_data = {
        'companys': ['카카오', '토스'], 'directors': ['김택윤', '이운기'], 'genreAlt': '테스트', 'movieCd': '2',
        'movieNm': '포스트테스트', 'movieNmEn': 'POSTTEST', 'nationAlt': '테스트', 'openDt': '20200101',
        'prdtStatNm': '테스트', 'prdtYear': '2020', 'typeNm': '장편',
    }
    api_response = api.post(
        '/movies',
        data=json.dumps(request_data),
        content_type="application/json"
    )

    assert api_response.status_code == 200

    api_response = api.get(
        '/movies/2'
    )
    payload = json.loads(api_response.data.decode('utf-8'))
    payload = {key: value for key, value in dict(payload).items()}

    assert api_response.status_code == 200

    response_data = {
        'companys': [{'id': 2, 'name': '카카오'}, {'id': 3, 'name': '토스'}],
        'directors': [{'id': 2, 'name': '김택윤'}, {'id': 3, 'name': '이운기'}],
        'genreAlt': '테스트', 'movieCd': '2', 'movieNm': '포스트테스트', 'movieNmEn': 'POSTTEST',
        'nationAlt': '테스트', 'openDt': '20200101', 'prdtStatNm': '테스트', 'prdtYear': '2020', 'typeNm': '장편'
    }

    assert payload == response(status='NORMAL', data=response_data, unit_test=True)


def test_movie_delete(api):
    response = Response()
    api_response = api.delete(
        '/movies/1',
    )

    assert api_response.status_code == 200

    api_response = api.get(
        '/movies/1',
    )

    payload = json.loads(api_response.data.decode('utf-8'))
    payload = {key: value for key, value in dict(payload).items()}

    print(payload)

    assert api_response.status_code == 200
    assert payload == response(status='NOT_FOUND', data='None', unit_test=True)
