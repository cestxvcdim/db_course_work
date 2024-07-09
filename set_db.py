import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()
db_user = os.getenv('DB_USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')

engine = create_engine(f"postgresql://{db_user}:{password}@{host}:{port}/{db_name}")
Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
