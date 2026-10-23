from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Cadastro


def select_todos_cadastros():
    # Buscar todos os equipamentos no banco
    # 1- Montar o select
    cadastros_sql = select(Cadastro)
    # 2- Executar o select
    cadastros = db_session.execute(cadastros_sql).all()
    return cadastros

def salvar(nome, data_nascimento, telefone, email, senha):
    # 3- Salvar no banco
    try:
        novo_cadastro = Cadastro(nome=nome, data_nascimento=data_nascimento, telefone=telefone, email=email, senha=senha)
        db_session.add(novo_cadastro)
        db_session.commit()
        flash("Usuário cadastrado com sucesso", "success")
        return novo_cadastro
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")