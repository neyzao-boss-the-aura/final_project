from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Funcionario


def select_todos_funcionario():
    # Buscar todos os times no banco
    # 1- Montar o select
    funcionarios_sql = (
    select(Funcionario)
)
    # join(Tabela que eu quero juntar, condição = Chave estrangeira == Chave primária)
    funcionario = db_session.execute(funcionarios_sql).scalars().all()
    return funcionario

def salvar(nome, email, telefone, endereco, contratado_em, estado):
    # 3- Salvar no banco
    try:
        novo_funcionario = Funcionario(nome=nome, email=email, telefone=telefone, endereco=endereco, contratado_em=contratado_em, estado=estado)
        db_session.add(novo_funcionario)
        db_session.commit()
        flash("Usuario criado com sucesso", "success")
        return novo_funcionario
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")

def select_um_funcionario(id_funcionario):
    funcionario_sql = select(Funcionario).where(Funcionario.id == id_funcionario)
    funcionario = db_session.execute(funcionario_sql).scalar_one_or_none()
    return funcionario
