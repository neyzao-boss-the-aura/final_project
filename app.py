from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from banco_dados import tabela_cadastro, tabela_equipamentos, tabela_servico, tabela_recurso
from database import *
from datetime import datetime
from templates import *

app = Flask(__name__)
app.secret_key = "chave-secreta-projeto-2026"

@app.route("/", methods=["GET", "POST"])
def inicio():
    return render_template("inicio.html")

@app.route("/cadastros", methods=["GET", "POST"])
def listar_cadastros():
    novo_cadastro = tabela_cadastro.select_todos_cadastros()
    return render_template("novo_cadastro.html", novo_cadastro=novo_cadastro)

@app.route("/equipamentos", methods=["GET", "POST"])
def listar_equipamentos():
    novo_equipamento = tabela_equipamentos.select_todos_equipamentos()
    return render_template("novo_equipamento.html", novo_equipamento=novo_equipamento)

@app.route("/recursos", methods=["GET", "POST"])
def listar_recursos():
    novo_recurso = tabela_recurso.select_todos_recursos()
    return render_template("novo_recurso.html", novo_recurso=novo_recurso)

@app.route("/ordem_servicos", methods=["GET", "POST"])
def listar_ordem_servicos():
    nova_ordem_servicos = tabela_servico.select_todos_ordem()
    return render_template("listar_ordem_servicos.html", nova_ordem_servicos=nova_ordem_servicos)

@app.route("/cadastro/novo", methods=["GET", "POST"])
def novo_cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        data_nascimento = request.form.get("data_nascimento", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not nome:
            flash('Por favor, insira o seu nome', 'error')
            return redirect(url_for("novo_cadastro"))
        if not data_nascimento:
            flash('Por favor, insira a sua data de nascimento', 'error')
            return redirect(url_for("novo_cadastro"))
        if not email:
            flash('Por favor, insira o seu email', 'error')
            return redirect(url_for("novo_cadastro"))
        if not telefone:
            flash('Por favor, insira o seu telefone', 'error')
            return redirect(url_for("novo_cadastro"))
        if not senha:
            flash('Por favor, insira a sua senha', 'error')
            return redirect(url_for("novo_cadastro"))

        tabela_cadastro.salvar(nome=nome, data_nascimento=data_nascimento, email=email, telefone=telefone, senha=senha)
        return redirect(url_for("novo_cadastro"))

    cadastro = tabela_cadastro.select_todos_cadastros()
    print(cadastro)
    return render_template("novo_cadastro.html", cadastro=cadastro)

@app.route("/equipamento/novo", methods=["GET", "POST"])
def novo_equipamento():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        usuario = request.form.get("cliente", "").strip()
        quantidade = request.form.get("quantidade", "").strip()
        nota_cliente = request.form.get("nota_cliente", "").strip()

        if not nome:
            flash('Por favor, insira o nome do equipamento', 'error')
            return redirect(url_for("novo_equipamento"))
        if not usuario:
            flash('Por favor, insira o seu nome', 'error')
            return redirect(url_for("novo_equipamento"))
        if not quantidade:
            flash('Por favor, insira a quantidade', 'error')
            return redirect(url_for("novo_equipamento"))
        if not nota_cliente:
            flash('Deixe uma nota de descrição (Não obrigatório)', 'error')
            return redirect(url_for("novo_equipamento"))

        tabela_equipamentos.salvar(nome=nome, usuario=usuario, quantidade=quantidade, nota_cliente=nota_cliente)
        return redirect(url_for("novo_equipamento"))

    equipamentos = tabela_equipamentos.select_todos_equipamentos()
    print(equipamentos)
    return render_template("listar_equipamentos.html", equipamentos=equipamentos)

@app.route("/recurso/novo", methods=["GET", "POST"])
def novo_recurso():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        equipamento = request.form.get("equipamento", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not nome:
            flash('Por favor, insira o nome do recurso', 'error')
            return redirect(url_for("novo_recurso"))
        if not responsavel:
            flash('Por favor, insira o responsável pelo recurso', 'error')
            return redirect(url_for("novo_recurso"))
        if not equipamento:
            flash('Por favor, insira o equipamento que será concertado', 'error')
            return redirect(url_for("novo_recurso"))
        if not descricao:
            flash('Deixe uma nota de descrição (Não obrigatório)', 'error')
            return redirect(url_for("novo_recurso"))

        tabela_recurso.salvar(nome=nome, responsavel=responsavel, equipamento=equipamento, descricao=descricao)
        return redirect(url_for("novo_recurso"))

    recursos = tabela_recurso.select_todos_recursos()
    print(recursos)
    return render_template("listar_recursos.html", novo_recurso=novo_recurso)

@app.route("/ordem_servicos/nova", methods=["GET", "POST"])
def nova_ordem_servicos():
    if request.method == "POST":
        usuario = request.form.get("cliente", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        equipamento = request.form.get("equipamento", "").strip()
        recurso = request.form.get("recurso", "").strip()
        prioridade = request.form.get("prioridade", "").strip()
        estado = request.form.get("estado", "").strip()
        data_abertura = request.form.get("data_abertura", "").strip()
        data_prazo = request.form.get("data_prazo", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not usuario:
            flash('Por favor, insira o usuario', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not responsavel:
            flash('Por favor, insira o nome do responsável', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not equipamento:
            flash('Por favor, insira o equipamento', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not recurso:
            flash('Por favor, insira o recurso', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not prioridade:
            flash('Por favor, insira a prioridade', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not estado:
            flash('Por favor, selecione o status da OS', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not data_abertura:
            flash('Por favor, insira a data de abertura', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not data_prazo:
            flash('Digite a data do prazo', 'error')
            return redirect(url_for("nova_ordem_servicos"))
        if not descricao:
            flash('Digite a descrição da OS', 'error')
            return redirect(url_for("nova_ordem_servicos"))

        tabela_servico.salvar(usuario=usuario, responsavel=responsavel, equipamento=equipamento, recurso=recurso, prioridade=prioridade, estado=estado, data_abertura=data_abertura, data_prazo=data_prazo, descricao=descricao)
        return redirect(url_for("nova_ordem_servicos"))

    nova_ordem_servicos = tabela_servico.select_todos_ordem()
    print(nova_ordem_servicos)
    return render_template("nova_ordem_servico.html", nova_ordem_servicos=nova_ordem_servicos)

if __name__ == "__main__":
    app.run(debug=True)