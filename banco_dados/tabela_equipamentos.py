from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Equipamento, Usuario

def select_todos_equipamentos():
    # Buscar todos os times no banco
    # 1- Montar o select
    # join(Tabela que eu quero juntar, condição = Chave estrangeira == Chave primária)
    equipamentos_sql = select(Equipamento)
    # 2- Executar o select
    equipamentos = db_session.execute(equipamentos_sql).scalars().all()
    return equipamentos

def salvar(nome, quantidade, nota_usuario):
    # 3- Salvar no banco
    try:
        novo_equipamento = Equipamento(nome=nome, quantidade=quantidade, nota_usuario=nota_usuario)
        db_session.add(novo_equipamento)
        db_session.commit()
        flash("Equipamento criado com sucesso", "success")
        return novo_equipamento
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")

def select_um_equipamento(id_equipamento):
    equipamento_sql = select(Equipamento).where(Equipamento.id == id_equipamento)
    equipamento = db_session.execute(equipamento_sql).scalar_one_or_none()
    return equipamento