'''
    AWS RDS (MY SQL) 정보
'''

db = {
    'user': 'root',
    'password': 'schwisestudy',
    'host': 'wisestudy.cinqw7ouyrxc.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'ticketplace'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"


'''
    unit test 진행 하기 위한
    AWS RDS (MY SQL) 정보
'''

test_db = {
    'user': 'root',
    'password': 'schwisestudy',
    'host': 'wisestudy.cinqw7ouyrxc.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'test_ticketplace'
}

test_config = {
    'DB_URL' : f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@" \
             f"{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8"
}


