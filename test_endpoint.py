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
    """), new_movie)
