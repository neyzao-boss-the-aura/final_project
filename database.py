import os
from datetime import date, datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine("mysql+pymysql://root:senaisp@localhost/projeto_final_2026")

db_session = scoped_session (sessionmaker(bind=engine))

Base = declarative_base()

class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    quantidade = Column(Integer, default=0)
    nota_usuario = Column(String(300), default=0)

    def __repr__(self):
        return f"{self.nome}"

class Ordem(Base):
    __tablename__ = "ordens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    responsavel = Column(String(50), nullable=False)
    prioridade = Column(String(50))
    estado = Column(String(50))
    data_abertura = Column(Date)
    data_prazo = Column(Date)
    descricao = Column(String(350))

    def __repr__(self):
        return f"{self.id}"

class Recurso(Base):
    __tablename__ = "recursos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    responsavel = Column(String(50), nullable=False)
    descricao = Column(String(300))

    def __repr__(self):
        return f"{self.nome}"

class Usuario(Base, UserMixin):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    #Senha
    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

    def __repr__(self):
        return f"{self.nome}"

class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    telefone = Column(Integer, nullable=False)
    endereco = Column(String(120), nullable=False)
    contratado_em = Column(Date)
    estado = Column(String(50), nullable=False)

    def __repr__(self):
        return f"{self.nome}"

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)