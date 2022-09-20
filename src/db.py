from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv


load_dotenv()
username = getenv('DB_USER')
password = getenv('DB_PASSWORD')
db_name = getenv('DB_NAME')
domain = getenv('DOMAIN')
host = getenv('HOST')

url = f'postgresql://{username}:{password}@{domain}:{host}/{db_name}'

Base = declarative_base()
engine = create_engine(url, echo=True, pool_size=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()
