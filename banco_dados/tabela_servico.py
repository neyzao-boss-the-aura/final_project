from flask import flash
from sqlalchemy import select, func, join
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_session, Ordem, Equipamento, Cadastro, Recurso

def select_todos_ordem():
    # Buscar todos as OS no banco
    # 1- Montar o select
    ordens_sql = (
    select(Ordem, Equipamento, Cadastro, Recurso)
    .join(Cadastro, Ordem.usuario == Cadastro.id)
    .join(Equipamento, Ordem.equipamento == Equipamento.id)
    .join(Recurso, Ordem.recurso == Recurso.id)
    )

    # 2- Executar o select
    ordens = db_session.execute(ordens_sql).all()
    return ordens

def salvar(usuario, responsavel, equipamento, recurso, prioridade, estado, data_abertura, data_prazo, descricao):
    # 3- Salvar no banco
    try:
        nova_ordem = Ordem(
            usuario=usuario, responsavel=responsavel,
            equipamento=equipamento, recurso=recurso,
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