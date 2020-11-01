### API LIST

### GET /movies

##### request query
- > page : 현재 페이지
- > per_page : 페이지당 movie data 갯수

##### response

- NORMAL
```json
    {
        "data": {
            "movies": [
                {
                    "genreAlt": "코미디",
                    "movieCd": "20078605",
                    "movieNm": "낙엽귀근",
                    "movieNmEn": "Getting Home",
                    "nationAlt": "중국",
                    "openDt": "20200924"
                },
                {
                    "genreAlt": "드라마",
                    "movieCd": "20080850",
                    "movieNm": "공포분자",
                    "movieNmEn": "The Terrorizers",
                    "nationAlt": "기타",
                    "openDt": "20200917"
                }
            ]
        },
        "message": "NORMAL",
        "pagination": {
            "limit": 258,
            "page": 2,
            "per_page": 2
        },
        "status": 200
    }
```

---

### GET /movies/{movie_id}
##### request

##### response

- NORMAL
```json
    {
        "data": {
            "companys": [],
            "directors": [
                {
                    "id": 109,
                    "name": "장양"
                }
            ],
            "genreAlt": "코미디",
            "movieCd": "20078605",
            "movieNm": "낙엽귀근",
            "movieNmEn": "Getting Home",
            "nationAlt": "중국",
            "openDt": "20200924",
            "prdtStatNm": "개봉",
            "prdtYear": "2008",
            "typeNm": "장편"
        },
        "message": "NORMAL",
        "status": 200
    }
```

- NOT_FOUND (movie_id를 찾지 못했을 때)
```json
{
    "data": "None",
    "message": "NOT_FOUND",
    "status": 404
}
```

---

### POST /movies
##### request body
```json
    {
        "companys": ["쇼박스"],
        "directors": ["장양"],
        "genreAlt": "코미디",
        "movieCd": "200786052",
        "movieNm": "낙엽귀근",
        "movieNmEn": "Getting Home",
        "nationAlt": "중국",
        "openDt": "20200924",
        "prdtStatNm": "개봉",
        "prdtYear": "2008",
        "typeNm": "장편"
    }
```

##### response

- NORMAL
```json
    {
        "data": {
            "companys": [
                "쇼박스"
            ],
            "directors": [
                "장양"
            ],
            "genreAlt": "코미디",
            "movieCd": "200786052",
            "movieNm": "낙엽귀근",
            "movieNmEn": "Getting Home",
            "nationAlt": "중국",
            "openDt": "20200924",
            "prdtStatNm": "개봉",
            "prdtYear": "2008",
            "typeNm": "장편"
        },
        "message": "CREATE",
        "status": 201
    }
```

- BAD_REQUEST (잘못된 데이터 입력)
```json
    {
        "data": "None",
        "message": "BAD_REQUEST",
        "status": 400
    }
```

- NOT_ACCEPTABLE (허용된 data type이 아닐때)
```json
    {
        "data": "None",
        "message": "NOT_ACCEPTABLE",
        "status": 406
    }
```
---

- CONFLICT (movie_id가 중복 되었을때)
```json
    {
        "data": "None",
        "message": "CONFLICT",
        "status": 409
    }
```
### PUT /movies
##### request body
```json
    {
        "companys": [{"id": 151, "companyNm": "쇼박스"}],
        "directors": [{"id": 418, "peopleNm" :  "장양"}],
        "genreAlt": "코미디",
        "movieCd": "1",
        "movieNm": "낙엽귀근",
        "movieNmEn": "Getting Home",
        "nationAlt": "중국",
        "openDt": "20200924",
        "prdtStatNm": "개봉",
        "prdtYear": "2008",
        "typeNm" : "장편"
    }
```
##### response

- NORMAL
```json
    {
        "data": {
            "companys": [
                {
                    "id": 151,
                    "name": "쇼박스"
                }
            ],
            "directors": [
                {
                    "id": 418,
                    "name": "장양"
                }
            ],
            "genreAlt": "코미디",
            "movieCd": "1",
            "movieNm": "낙엽귀근",
            "movieNmEn": "Getting Home",
            "nationAlt": "중국",
            "openDt": "20200924",
            "prdtStatNm": "개봉",
            "prdtYear": "2008",
            "typeNm": "장편"
        },
        "message": "NORMAL",
        "status": 200
    }
```
- BAD_REQUEST (잘못된 데이터 입력)
```json
    {
        "data": "None",
        "message": "BAD_REQUEST",
        "status": 400
    }
```

- NOT_ACCEPTABLE (허용된 data type이 아닐때)
```json
    {
        "data": "None",
        "message": "NOT_ACCEPTABLE",
        "status": 406
    }
```
---
### DELETE /movies/{movie_id}
##### response
- NORMAL
```json
    {
        "data": "1",
        "message": "NORMAL",
        "status": 200
    }
```

---

### 모든 API

##### response
- METHOD_NOT_ALLOWED(해당 end point에 허용되지 않은 method를 호출 할때)
```json
    {
        "data": "None",
        "message": "METHOD_NOT_ALLOWED",
        "status": 405
    }
```