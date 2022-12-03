from sqlalchemy import Column, String
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql+mysqldb://root:1234@localhost/dw_alunos')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Fato01(Base):
    __tablename__ = 'fato01'

    cpf = Column(String(255), primary_key=True, nullable=True)
    etnia = Column(String(255), nullable=True)
    genero = Column(String(1), nullable=True)
    renda = Column(String(255), nullable=True)
    escola_origem = Column(String(255), nullable=True)
    estado = Column(String(255), nullable=True)
    cidade = Column(String(255), nullable=True)
    faixa_etaria = Column(String(255), nullable=True)
    matricula_situacao = Column(String(255), nullable=True)


def get_dados_sum(tipo):
    return session.query(
        eval(f'Fato01.{tipo}'),
        func.count().label('total')
    ).group_by(eval(f'Fato01.{tipo}')).all()
