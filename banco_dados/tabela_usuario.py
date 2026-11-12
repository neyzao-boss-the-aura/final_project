from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Usuario


def select_todos_usuarios():
    # Buscar todos os times no banco
    # 1- Montar o select
    usuarios_sql = (
    select(Usuario)
)
    # join(Tabela que eu quero juntar, condição = Chave estrangeira == Chave primária)
    usuario = db_session.execute(usuarios_sql).all()
    return usuario

def salvar(nome, email, senha_hash, atualizado_em, criado_em):
    # 3- Salvar no banco
    try:
        novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, atualizado_em=atualizado_em, criado_em=criado_em)
        db_session.add(novo_usuario)
        db_session.commit()
        flash("Usuario criado com sucesso", "success")
        return novo_usuario
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")
