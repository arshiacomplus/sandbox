from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DB_URL

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

    github_token = Column(String, nullable=True)       
    github_repo = Column(String, nullable=True)        

Base.metadata.create_all(engine)