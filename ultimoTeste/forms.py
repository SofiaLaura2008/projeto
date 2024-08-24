from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ultimoTeste.models import Cliente

class RegistrationForm(FlaskForm):
    nomeSobrenome = StringField('Nome e Sobrenome: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    celular = StringField('Celular: ', validators=[DataRequired()])
    sexo = SelectField('Sexo: ', choices=[
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('prefiro_nao_dizer', 'Prefiro não dizer')
    ], validators=[DataRequired()])
    password = PasswordField('Senha: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme a Senha: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

    def validate_nomeSobrenome(self, nomeSobrenome):
        user = Cliente.query.filter_by(nome_e_sobrenome=nomeSobrenome.data).first()
        if user:
            raise ValidationError('Esse nome já está em uso. Escolha outro.')

    def validate_email(self, email):
        user = Cliente.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Esse email já está registrado. Por favor, use um diferente.')

class ProdutoForm(FlaskForm):
    nomeProduto = StringField('Nome do Produto', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    preco = FloatField('Preço', validators=[DataRequired()])
    categoriaId = SelectField('Categoria', coerce=int, choices=[
        ('1', 'Brinquedos'),
        ('2', 'Banho'),
        ('3', 'Rações')
    ])  
    estoque = IntegerField('Estoque', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')