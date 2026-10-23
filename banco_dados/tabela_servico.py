from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import *


def select_todos():
    return None

def salvar_ordem(cliente, responsavel, recurso, prioridade, estado, data_abertura, data_prazo, equipamento, descricao):
    return None