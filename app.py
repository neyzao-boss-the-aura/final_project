from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from banco_dados import tabela_equipamentos, tabela_servico, tabela_recurso, tabela_funcionario
from database import *
from functools import wraps
from datetime import datetime
from templates import *

app = Flask(__name__)
app.secret_key = "chave-secreta-projeto-2026"



# SITUAÇÃO ATUAL: CONFIGURANDO O EDITAR
# PENDÊNCIAS: TERMINAR HTML DOS FORMULÁRIOS COM LISTAS,
# DETALHES E RELATÓRIO, CHAVES ESTRANGEIRAS DO BANCO COM LISTAS AUXILIARES



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

def roles_required (*papeis_permitidos):
    # Decorator para restringir acesso baseado no papel do usuário logado
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.papel not in papeis_permitidos:
                flash("Acesso negado: Você não tem permissão para acessar esta página", "error")
                return redirect(url_for("inicio"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#Interface de autenticação a
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
            return redirect(url_for('login'))

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
    print(novo_equipamento)
    return render_template("listar_equipamentos.html", equipamentos=novo_equipamento)

@app.route("/funcionarios", methods=["GET", "POST"])
def listar_funcionarios():
    novo_funcionario = tabela_funcionario.select_todos_funcionario()
    return render_template("listar_funcionarios.html", funcionarios=novo_funcionario)

@app.route("/recursos", methods=["GET", "POST"])
def listar_recursos():
    novo_recurso = tabela_recurso.select_todos_recursos()
    return render_template("listar_recursos.html", recursos=novo_recurso)

@app.route("/ordem_servicos", methods=["GET", "POST"])
def listar_ordem_servicos():
    nova_ordem_servicos = tabela_servico.select_todos_ordem()
    return render_template("listar_ordem_servicos.html", ordem_servicos=nova_ordem_servicos)

@app.route("/equipamento/novo", methods=["GET", "POST"])
@roles_required("admin")
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
    print(equipamentos_lista)
    return render_template("novo_equipamento.html", equipamentos=equipamentos_lista)

@app.route("/equipamentos/<id_equipamento>", methods=["GET", "POST"])
@roles_required("admin")
def editar_equipamento(id_equipamento):
    #Buscar o jogador no banco
    equipamento = tabela_equipamentos.select_um_equipamento(id_equipamento)
    #Salvar as alterações
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        quantidade = request.form.get("quantidade") or None
        nota_usuario = request.form.get("nota_usuario", "").strip()

        # 2- Verificar se foi digitado
        if not nome:
            flash("PREENCHA O NOME", "error")
        elif not quantidade:
            flash("PREENCHA A QUANTIDADE", "error")
        elif not nota_usuario:
            flash("PREENCHA A NOTA DO USUÁRIO", "error")
        else:
            equipamento.nome = nome
            equipamento.quantidade = quantidade
            equipamento.nota_usuario = nota_usuario
            db_session.commit()

    #Carregar as informações
    equipamentos = tabela_equipamentos.select_todos_equipamentos()
    return render_template("listar_equipamentos.html", equipamentos=equipamentos, editar = editar_equipamento)

@app.route("/recurso/novo", methods=["GET", "POST"])
@roles_required("admin")
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

@app.route("/recursos/<id_recurso>", methods=["GET", "POST"])
@roles_required("admin")
def editar_recurso(id_recurso):
    #Buscar o jogador no banco
    recurso = tabela_recurso.select_um_recurso(id_recurso)
    #Salvar as alterações
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel") or None
        descricao = request.form.get("descricao", "").strip()

        # 2- Verificar se foi digitado
        if not nome:
            flash("PREENCHA O NOME", "error")
        elif not responsavel:
            flash("PREENCHA O RESPONSÁVEL", "error")
        elif not descricao:
            flash("PREENCHA A DESCRIÇÃO", "error")
        else:
            recurso.nome = nome
            recurso.responsavel = responsavel
            recurso.descricao = descricao
            db_session.commit()

    #Carregar as informações
    recursos = tabela_recurso.select_todos_recursos()
    return render_template("listar_recursos.html", recursos=recursos, editar = editar_recurso)

@app.route("/ordem_servicos/nova", methods=["GET", "POST"])
@roles_required("admin")
def nova_ordem_servicos():
    if request.method == "POST":
        responsavel = request.form.get("responsavel", "").strip()
        prioridade = request.form.get("prioridade", "").strip()
        estado = request.form.get("estado", "").strip()
        data_abertura = request.form.get("data_abertura", "").strip()
        data_prazo = request.form.get("data_prazo", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not responsavel:
            flash('Por favor, insira o nome do responsável', 'error')
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

        tabela_servico.salvar(responsavel=responsavel, prioridade=prioridade, estado=estado, data_abertura=data_abertura, data_prazo=data_prazo, descricao=descricao)
        return redirect(url_for("nova_ordem_servicos"))

    nova_ordem_servicos = tabela_servico.select_todos_ordem()
    print(nova_ordem_servicos)
    return render_template("nova_ordem_servico.html", nova_ordem_servicos=nova_ordem_servicos)

@app.route("/ordem_servicos/<id_ordem_servico>", methods=["GET", "POST"])
@roles_required("admin")
def editar_ordem_servicos(id_ordem_servico):
    #Buscar o jogador no banco
    ordem_servico = tabela_servico.select_um_ordem_servico(id_ordem_servico)
    #Salvar as alterações
    if request.method == "POST":
        responsavel = request.form.get("responsavel", "").strip()
        prioridade = request.form.get("prioridade", "").strip()
        estado = request.form.get("estado", "").strip()
        data_abertura = request.form.get("data_abertura", "").strip()
        data_prazo = request.form.get("data_prazo", "").strip()
        descricao = request.form.get("descricao", "").strip()

        # 2- Verificar se foi digitado
        if not responsavel:
            flash('Por favor, insira o nome do responsável', 'error')
        if not prioridade:
            flash('Por favor, insira a prioridade', 'error')
        if not estado:
            flash('Por favor, selecione o status da OS', 'error')
        if not data_abertura:
            flash('Por favor, insira a data de abertura', 'error')
        if not data_prazo:
            flash('Digite a data do prazo', 'error')
        if not descricao:
            flash('Digite a descrição da OS', 'error')
        else:
            ordem_servico.responsavel = responsavel
            ordem_servico.prioridade = prioridade
            ordem_servico.estado = estado
            ordem_servico.data_abertura = data_abertura
            ordem_servico.data_prazo = data_prazo
            ordem_servico.descricao = descricao
            db_session.commit()

    #Carregar as informações
    ordem_servicos = tabela_servico.select_todos_ordem()
    return render_template("listar_ordem_servicos.html", ordem_servicos=ordem_servicos, editar = editar_ordem_servicos)

@app.route("/funcionario/novo", methods=["GET", "POST"])
@roles_required("admin")
def novo_funcionario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        endereco = request.form.get("endereco", "").strip()
        contratado_em = request.form.get("contratado_em", "").strip()
        estado = request.form.get("estado", "").strip()

        if not nome:
            flash('Por favor, insira o nome', 'error')
            return redirect(url_for("novo_funcionario"))
        if not email:
            flash('Por favor, insira o email', 'error')
            return redirect(url_for("novo_funcionario"))
        if not telefone:
            flash('Por favor, insira o telefone', 'error')
            return redirect(url_for("novo_funcionario"))
        if not endereco:
            flash('Por favor, insira o endereco', 'error')
            return redirect(url_for("novo_funcionario"))
        if not contratado_em:
            flash('Por favor, insira o contratado em', 'error')
            return redirect(url_for("novo_funcionario"))
        if not estado:
            flash('Por favor, selecione o estado', 'error')
            return redirect(url_for("novo_funcionario"))

        tabela_funcionario.salvar(nome=nome, email=email, telefone=telefone, endereco=endereco, contratado_em=contratado_em, estado=estado)
        return redirect(url_for("novo_funcionario"))

    funcionarios = tabela_funcionario.select_todos_funcionario()
    print(funcionarios)
    return render_template("novo_funcionario.html", funcionarios=funcionarios)

@app.route("/funcionarios/<id_funcionario>", methods=["GET", "POST"])
@roles_required("admin")
def editar_funcionarios(id_funcionario):
    #Buscar o jogador no banco
    funcionario = tabela_funcionario.select_um_funcionario(id_funcionario)
    #Salvar as alterações
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        endereco = request.form.get("endereco", "").strip()
        contratado_em = request.form.get("contratado_em", "").strip()
        estado = request.form.get("estado", "").strip()

        if not nome:
            flash('Por favor, insira o nome', 'error')
        if not email:
            flash('Por favor, insira o email', 'error')
        if not telefone:
            flash('Por favor, insira o telefone', 'error')
        if not endereco:
            flash('Por favor, insira o endereco', 'error')
        if not contratado_em:
            flash('Por favor, insira o contratado em', 'error')
        if not estado:
            flash('Por favor, selecione o estado', 'error')
        else:
            funcionario.nome = nome
            funcionario.email = email
            funcionario.telefone = telefone
            funcionario.endereco = endereco
            funcionario.contratado_em = contratado_em
            funcionario.estado = estado
            db_session.commit()

    #Carregar as informações
    funcionarios = tabela_funcionario.select_todos_funcionario()
    return render_template("listar_funcionarios.html", funcionarios=funcionarios, editar = editar_funcionarios)

if __name__ == "__main__":
    app.run(debug=True)