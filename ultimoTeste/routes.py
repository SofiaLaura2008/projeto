from flask import render_template, url_for, flash, redirect, request, session
from ultimoTeste import app, db, login_manager
from ultimoTeste.forms import RegistrationForm, ProdutoForm
from werkzeug.security import generate_password_hash, check_password_hash
from ultimoTeste.models import Cliente, Produtos, Categorias
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def home():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        cliente = Cliente.query.filter_by(email=email).first()
        
        if cliente and check_password_hash(cliente.senha, senha):
            login_user(cliente)  # Usando Flask-Login
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Conta não encontrada ou senha incorreta.', 'warning')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_client = Cliente(
            nome_e_sobrenome=form.nomeSobrenome.data,
            email=form.email.data,
            senha=hashed_password,
            celular=form.celular.data,
            sexo=form.sexo.data
        )
        db.session.add(new_client)
        db.session.commit()
        flash('Sua conta foi criada! Você pode agora fazer login.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html', title='Cadastrar', form=form)

@app.route('/perfil')
@login_required  
def perfil():
    cliente = current_user 
    return render_template('perfil.html', cliente=cliente)

@app.route('/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar_usuario():
    if request.method == 'POST':
        cliente = current_user
        cliente.nome_e_sobrenome = request.form['nome']
        cliente.email = request.form['email']
        if request.form['senha']:  # Atualiza a senha apenas se fornecida
            cliente.senha = generate_password_hash(request.form['senha'])
        cliente.sexo = request.form['sexo']
        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('perfil'))
    
    return render_template('atualizar.html')

@app.route('/deletar', methods=['GET', 'POST'])
@login_required
def deletar_usuario():
    if request.method == 'POST':
        cliente = current_user
        db.session.delete(cliente)
        db.session.commit()
        flash('Usuário deletado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('deletar.html')

@app.route('/produtos', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    form = ProdutoForm()
    form.categoriaId.choices = [(c.id, c.nomeCategorias) for c in Categorias.query.all()]

    if not categorias:
        flash('Nenhuma categoria disponível. Por favor, adicione categorias antes de cadastrar produtos.', 'warning')
        return redirect(url_for('adicionar_categoria'))

    if form.validate_on_submit():
        novo_produto = Produtos(
            nomeProduto=form.nomeProduto.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            categoriaId=form.categoriaId.data,
            estoque=form.estoque.data
        )
        
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('adicionar_produto'))

    return render_template('produtos.html', form=form)

@app.route('/lista_produtos')
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)