from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from banco_dados import tabela_equipamentos, tabela_servico, tabela_recurso, tabela_usuario
from database import *
from datetime import datetime
from templates import *

app = Flask(__name__)
app.secret_key = "chave-secreta-projeto-2026"

@app.route("/")
@login_required
def inicio ():
    return render_template("inicio.html")

#Configurar Flask-login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar"

#Prevenir gargalo "too many connections"
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#Carregar informações do usuário logado
@login_manager.user_loader
def load_user(user_id):
    return db_session.get(Usuario, int(user_id))

#Interface de autenticação
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("senha", "").strip()

        usuario_sql = select(Usuario).where(Usuario.email == email)
        usuario_resultado = db_session.execute(usuario_sql).scalar()

        if not usuario_resultado:
            flash("Falha ao autenticar", "error")
            return render_template("login.html")

        if usuario_resultado and usuario_resultado.check_password(password):
            login_user(usuario_resultado)
            return redirect(url_for("inicio"))

    return render_template(
        "login.html",
        registro= request.args.get("registro") == 'True')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not nome and not email and not senha :
            flash("PREENCHA OS CAMPOS", "error")
            return redirect (url_for("registro"))

        usuario_sql = select(Usuario).where (Usuario.email == email)
        usuario_email = db_session.execute(usuario_sql).scalars().all()

        if usuario_email:
            flash("Email já cadastrado")
            return redirect (url_for("registro"))
        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email)

            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash("Usuario cadastrado com sucesso", "success")

        except SQLAlchemyError as e:
            print(f"SQLAlchemyError: {e}")
            flash("Erro no banco")
            pass
        except Exception as e:
            print(f"Erro ao registrar: {e}")
            flash("Erro ao registrar", "error")
            return redirect (url_for("registro"))
        return render_template("login.html")

@app.route("/equipamentos", methods=["GET", "POST"])
def listar_equipamentos():
    novo_equipamento = tabela_equipamentos.select_todos_equipamentos()
    return render_template("novo_equipamento.html", equipamentos=novo_equipamento)

@app.route("/recursos", methods=["GET", "POST"])
def listar_recursos():
    novo_recurso = tabela_recurso.select_todos_recursos()
    return render_template("listar_recursos.html", novo_recurso=novo_recurso)

@app.route("/usuarios", methods=["GET", "POST"])
def listar_usuarios():
    novo_usuario = tabela_usuario.select_todos_usuarios()
    return render_template("listar_usuarios.html", novo_usuario=novo_usuario)

@app.route("/ordem_servicos", methods=["GET", "POST"])
def listar_ordem_servicos():
    nova_ordem_servicos = tabela_servico.select_todos_ordem()
    return render_template("listar_ordem_servicos.html", nova_ordem_servicos=nova_ordem_servicos)

@app.route("/equipamento/novo", methods=["GET", "POST"])
def novo_equipamento():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        quantidade = request.form.get("quantidade", "").strip()
        nota_usuario = request.form.get("nota_usuario", "").strip()

        if not nome:
            flash('Por favor, insira o nome do equipamento', 'error')
            return redirect(url_for("novo_equipamento"))
        if not quantidade:
            flash('Por favor, insira a quantidade', 'error')
            return redirect(url_for("novo_equipamento"))
        if not nota_usuario:
            flash('Deixe uma nota  ', 'error')
            return redirect(url_for("novo_equipamento"))

        tabela_equipamentos.salvar(nome=nome, quantidade=quantidade, nota_usuario=nota_usuario)
        return redirect(url_for("novo_equipamento"))

    equipamentos_lista = tabela_equipamentos.select_todos_equipamentos()
    usuarios_lista = tabela_usuario.select_todos_usuarios()
    print(equipamentos_lista)
    print(usuarios_lista)
    return render_template("listar_equipamentos.html", equipamentos=equipamentos_lista)

@app.route("/recurso/novo", methods=["GET", "POST"])
def novo_recurso():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not nome:
            flash('Por favor, insira o nome do recurso', 'error')
            return redirect(url_for("novo_recurso"))
        if not responsavel:
            flash('Por favor, insira o responsável pelo recurso', 'error')
            return redirect(url_for("novo_recurso"))
        if not descricao:
            flash('Deixe uma nota de descrição (Não obrigatório)', 'error')
            return redirect(url_for("novo_recurso"))

        tabela_recurso.salvar(nome=nome, responsavel=responsavel, descricao=descricao)
        return redirect(url_for("novo_recurso"))

    recursos = tabela_recurso.select_todos_recursos()
    print(recursos)
    return render_template("novo_recurso.html", novo_recurso=recursos)

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
    novo_recurso = tabela_recurso.select_todos_recursos()
    novo_equipamento = tabela_equipamentos.select_todos_equipamentos()
    novo_usuario = tabela_usuario.select_todos_usuarios()
    print(nova_ordem_servicos)
    print(novo_recurso)
    print(novo_equipamento)
    print(novo_usuario)
    return render_template("nova_ordem_servico.html", nova_ordem_servicos=nova_ordem_servicos, novo_recurso=novo_recurso, novo_equipamento=novo_equipamento, novo_usuario=novo_usuario)

@app.route("/usuario/novo1", methods=["GET", "POST"])
def novo_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha_hash = request.form.get("senha_hash", "").strip()

        if not nome:
            flash("Digite o nome", "error")
            return redirect(url_for("novo_usuario"))
        if not email:
            flash("Digite o email", "error")
            return redirect(url_for("novo_usuario"))
        if not senha_hash:
            flash("Digite a senha", "error")
            return redirect(url_for("novo_usuario"))

        tabela_usuario.salvar(nome=nome, email=email, senha_hash=senha_hash)
        return redirect(url_for("novo_usuario"))

    usuario = tabela_usuario.select_todos_usuarios()
    print(usuario)

    return render_template("novo_usuario.html", novo_usuario=usuario )

if __name__ == "__main__":
    app.run(debug=True)