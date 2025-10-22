from flask_sqlalchemy import SQLAlchemy

# Inicializa o SQLAlchemy
db = SQLAlchemy()

# Modelo de Usuário
class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


# Modelo de Conversa
class Conversa(db.Model):
    __tablename__ = "conversa"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    mensagem_usuario = db.Column(db.Text, nullable=False)
    mensagem_bot = db.Column(db.Text, nullable=False)

    # Relacionamento: um usuário pode ter várias conversas
    usuario = db.relationship("Usuario", backref=db.backref("conversas", lazy=True))

    def __init__(self, usuario_id, mensagem_usuario, mensagem_bot):
        self.usuario_id = usuario_id
        self.mensagem_usuario = mensagem_usuario
        self.mensagem_bot = mensagem_bot
