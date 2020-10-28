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