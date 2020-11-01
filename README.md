# Ticket-Place
티켓 플레이스 과제

### API LIST
- GET /movies
- GET /movies/{movie_id}
- POST /movies
- PUT /movies
- DELETE /movies/{movie_id}

---

### 개발 환경
> - Python3.7
> - Flask
> - MySQL

---

### 프로젝트 초기화/ 빌드/ 테스트
g
##### 초기화 
- python 가상환경 생성
> - python -m venv {가상환경 이름}

- 가상환경 진입
> - source {가상환경 이름}/Scripts/activate

- 프로젝트 실행에 필요한 패키지 설치
> - pip install -r requirements.txt

##### 빌드
- flask app 실행
> - flaks run



##### 테스트
- GET /movie
> - curl -X GET http://127.0.0.1:5000/movies
>
- GET /movie/{movie_id}
> - curl -X GET http://127.0.0.1:5000/movies/{movie_id}

- POST /movie
> - curl -X POST -H "Content-Type: application/json" -d "{\"companys\": [\"{companys}\"], \"directors\": [\"{directors}\"], \"genreAlt\": \"{genreAlt}\", \"movieCd\": \"{movieCd}\", \"movieNm\": \"{movieNm}\", \"movieNmEn\": \"{movieNmEn}\", \"nationAlt\": \"{nationAlt}\", \"openDt\": \"{openDt}\", \"prdtStatNm\": \"{prdtStatNm}\", \"prdtYear\": \"{prdtYear}\",\"typeNm\": \"{typeNm}\"}" http://127.0.0.1:5000/movies

- PUT /movie
> - curl -X PUT -H "Content-Type: application/json" -H "Accept: application/json" -d "{\"companys\": [{\"id\": {id}, \"companyNm\": "\{companyNm}\"}\"}], \"directors\": [{\"id\": {id}}, \"peopleNm\": \"{peopleNm}\"}], \"genreAlt\": \"{genreAlt}\", \"movieCd\": \"{movieCd}\", \"movieNm\": \"{movieNm}\", \"movieNmEn\": \"{movieNmEn}\", \"nationAlt\": \"{nationAlt}\", \"openDt\": \"{openDt}\", \"prdtStatNm\": \"{prdtStatNm}\", \"prdtYear\": \"{prdtYear}\",\"typeNm\": \"{typeNm}\"}" http://127.0.0.1:5000/movies 

- DELETE /movie
> - curl -X DELETE http://127.0.0.1:5000/movies/{movie_id}
 
---

### unit test
- pytest를 이용하여 각 API에 대한 unit test를 진행 하였습니다.
- test_code 실행 방법
> - python -mpytest -vv -s -p no:warnings

---
### git branch 전략
##### master, develop, feature brach로 나누어 개발
- API 기능별로 feature branch를 만들어 작업 진행
- 완성된 기능을 develp branch에 merge
- 최종적으로 master branch에 merge하여 배포