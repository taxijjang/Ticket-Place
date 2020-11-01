import urllib.request
import pymysql
import json

'''
     영화 진흥원 OPNE API에서 데이터를 가지고와 AWS RDS (MY SQL)에 저장 하여 API 작성 준비
'''
MY_KEY = "6f71e3974aa22a1e6bf53a00798c933b"

conn = pymysql.connect(host='wisestudy.cinqw7ouyrxc.ap-northeast-2.rds.amazonaws.com', user='root',
                       passwd='schwisestudy', db='ticketplace')

cur = conn.cursor()

page_cnt = 0
while True:
    page_cnt += 1
    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={MY_KEY}&openStartDt=2020&itemPerPage=100&curPage={page_cnt}"
    data = urllib.request.urlopen(url).read().decode("utf-8")
    output = json.loads(data)

    movies = output['movieListResult']['movieList']
    movies_totCnt = output['movieListResult']['totCnt']

    if movies_totCnt == 0:
        break

    for movie in movies:
        if len(movie['movieNmEn']) == 0 or "성인물(에로)" in movie['genreAlt'] or "멜로/로맨스" in movie['genreAlt']:
            continue

        sql = f"INSERT INTO `movies` (movieCd, movieNm, movieNmEn, prdtYear, openDt,typeNm,prdtStatNm,nationAlt, genreAlt)\
                  VALUES('{movie['movieCd']}', '{movie['movieNm']}','{movie['movieNmEn']}','{movie['prdtYear']}','{movie['openDt']}',\
                 '{movie['typeNm']}','{movie['prdtStatNm']}','{movie['nationAlt']}', '{movie['genreAlt']}') ; "
        try:
            cur.execute(sql)
            conn.commit()

        except Exception as ex:
            print(f"movie error -> {ex}")

        for director in movie['directors']:
            print(director)
            sql = f"INSERT INTO `directors` (movieCd, peopleNm) VALUES ('{movie['movieCd']}', '{director['peopleNm']}'); "

            try:
                cur.execute(sql)
                conn.commit()
            except Exception as ex:
                print(f"director error -> {ex}")

        for company in movie['companys']:
            print(company)
            sql = f"INSERT INTO `companys` (movieCd, companyNm) VALUES ('{movie['movieCd']}', '{company['companyNm']}'); "

            try:
                cur.execute(sql)
                conn.commit()
            except Exception as ex:
                print(f"company error -> {ex}")


