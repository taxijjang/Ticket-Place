# Ticket-Place
티켓 플레이스 과제

---
### 개발 환경
> - Python3.7
> - Flask
> - MySQL
---
### 프로젝트 초기화/ 빌드/ 테스트

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
> -

- PUT /movie
> -

- DELETE /movie
> - 
 
---

### git branch 전략
> 1. master, develop, feature brach로 나누어 개발

