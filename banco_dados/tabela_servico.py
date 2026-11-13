from flask import flash
from sqlalchemy import select, func, join
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Ordem

def select_todos_ordem():
    # Buscar todos as OS no banco
    # 1- Montar o select

    ordens_sql = select (Ordem)

    # 2- Executar o select
    ordens = db_session.execute(ordens_sql).scalars().all()
    return ordens

def salvar( responsavel, prioridade, estado, data_abertura, data_prazo, descricao):
    # 3- Salvar no banco
    try:
        nova_ordem = Ordem(
            responsavel=responsavel,
            prioridade=prioridade, estado=estado,
            data_abertura=data_abertura, data_prazo=data_prazo, descricao=descricao)
        db_session.add(nova_ordem)
        db_session.commit()
        flash("Ordem de Serviço criada com sucesso", "success")
        return nova_ordem
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"{e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")

def select_um_ordem_servico(id_ordem_servico):
    ordem_servico_sql = select(Ordem).where(Ordem.id == id_ordem_servico)
    ordem_servico = db_session.execute(ordem_servico_sql).scalar_one_or_none()
    return ordem_servico