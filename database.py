import os
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session

engine = create_engine("mysql+pymysql://root:senaisp@localhost:3306/projeto_final_2026")

db_session = scoped_session (sessionmaker(bind=engine))

Base = declarative_base()

class Cadastro(Base):
    __tablename__ = "cadastros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    data_nascimento = Column(Date)
    email = Column(String(100))
    telefone = Column(Integer)
    senha = Column(String(50))

class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    usuario = Column(String(50), default=0)
    quantidade = Column(Integer, default=0)
    nota_cliente = Column(String(300), default=0)

class Ordem(Base):
    __tablename__ = "ordem_servicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(String(50), nullable=False)
    responsavel = Column(String(50), nullable=False)
    equipamento = Column(String(50))
    recurso = Column(String(50))
    prioridade = Column(String(50))
    estado = Column(String(50))
    data_abertura = Column(Date)
    data_prazo = Column(Date)
    descricao = Column(String(350))

class Recurso(Base):
    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    responsavel = Column(String(50), nullable=False)
    equipamento = Column(String(50))
    descricao = Column(String(300))

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)