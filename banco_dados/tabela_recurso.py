from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Recurso, Equipamento

def select_todos_recursos():
    # Buscar todos os times no banco
    # 1- Montar o select
    # join(Tabela que eu quero juntar, condição = Chave estrangeira == Chave primária)
    recursos_sql = select(Recurso, Equipamento).join(Equipamento, Recurso.equipamento == Equipamento.id).join(Recurso)
    # 2- Executar o select
    recursos = db_session.execute(recursos_sql).all()
    return recursos

def salvar(nome, responsavel, equipamento, descricao):
    # 3- Salvar no banco
    try:
        novo_recurso = Recurso(nome=nome, responsavel=responsavel, equipamento=equipamento, descricao=descricao)
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