from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOSTNAME = '192.168.212.131'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

Db_Uri = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, DATABASE)
print(Db_Uri)
engine = create_engine(Db_Uri)
Base = declarative_base(engine)
Session = sessionmaker(engine)
session = Session()


if __name__ == '__main__':
    connection = engine.connect()
    res = connection.execute('select 1')
    print(res.fetchone())



