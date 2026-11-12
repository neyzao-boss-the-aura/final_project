from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Recurso, Equipamento

def select_todos_usuarios():
    # Buscar todos os times no banco
    # 1- Montar o select
    recursos_sql = (
    select(Recurso)
)
    # join(Tabela que eu quero juntar, condição = Chave estrangeira == Chave primária)
    recursos = db_session.execute(recursos_sql).all()
    return recursos
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    atualizado_em = Column(DateTime, onupdate=func.now())
    criado_em = Column(DateTime, onupdate=func.now())
def salvar(nome, email, senha_hash, atualizado_em descricao):
    # 3- Salvar no banco
    try:
        novo_recurso = Recurso(nome=nome, responsavel=responsavel, descricao=descricao)
        db_session.add(novo_recurso)
        db_session.commit()
        flash("Recurso criado com sucesso", "success")
        return novo_recurso
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")
