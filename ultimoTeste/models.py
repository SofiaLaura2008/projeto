from ultimoTeste import db
from flask_login import UserMixin

class Cliente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_e_sobrenome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    sexo = db.Column(db.String(10), nullable=False) 

    def __repr__(self):
        return f"Cliente('{self.nome_e_sobrenome}', '{self.email}', '{self.celular}', '{self.sexo}')"

class Categorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomeCategorias = db.Column(db.String(80), nullable=False)

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomeProduto = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float(10, 2), nullable=False)
    categoriaId = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

    categoria = db.relationship('Categorias', backref='produtos')

class Pedidos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float(10, 2), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data_compra = db.Column(db.Date, nullable=False)

    cliente = db.relationship('Cliente', backref='pedidos')

class ItensPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)

    produto = db.relationship('Produtos', backref='itens')
    pedido = db.relationship('Pedidos', backref='itens')

@app.route('/lista_produtos')
def listar_produtos():
    produtos = Produtos.query.all()
    return render_template('produtos.html', produtos=produtos)
