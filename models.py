from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

USUARIO = 'postgres'
SENHA = 'root'
HOST = 'localhost'
BANCO = 'aaa'
PORTA = '5432'
CONN = f'postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}'

engine = create_engine(CONN, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
Base = declarative_base()


class Pessoa(Base):
    __tablename__ = 'Pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    user = Column(String(20))
    senha = Column(String(10))


class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('Pessoa.id'))
    token = Column(String(100))
    data = Column(DateTime, default=datetime.datetime.utcnow())


Base.metadata.create_all(engine)
