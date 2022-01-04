from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import CONN, Pessoa, Tokens
from secrets import token_hex
from fastapi import  FastAPI

app = FastAPI()

def connectBanco():
    engine = create_engine(CONN, echo = True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.post('/cadastro')
def cadastro(nome: str, user : str, senha : str):
    session = connectBanco()
    usuario = session.query(Pessoa).filter_by(user = user, senha = senha).all()
    if len(usuario) == 0:
        x = Pessoa(nome = nome, user = user, senha = senha)
        session.add(x)
        session.commit()
        return {'status':'sucesso'}
    elif len(usuario) > 0:
        return {'status':'usuario já cadastrado'}

@app.post('/login')
def login(user: str, senha: str):
    session = connectBanco()
    usuario = session.query(Pessoa).filter_by(user = user, senha = senha).all()
    if len(usuario) == 0:
        return {'status': 'usuario inexistente'}
    while True:
        token = token_hex(50)
        tokenExist = session.query(Tokens).filter_by(token=token).all()
        if len(tokenExist) == 0:
            pessoaExist = session.query(Tokens).filter_by(id_pessoa=usuario[0].id).all()
            if len(pessoaExist) == 0:
                novoToken = Tokens(id_pessoa=usuario[0].id, token=token)
                session.add(novoToken)
            elif len(pessoaExist) > 0:
                pessoaExist[0].tokens = token
            session.commit()
            break
        return token