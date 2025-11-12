from flask import Flask
from flask_cors import CORS
from models import db
from routes import initialize_routes

app = Flask(__name__)
CORS(app)

# Configuração do MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/humora'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

# Inicializa o banco
db.init_app(app)

# Inicializa as rotas
initialize_routes(app)

# Cria tabelas (se não existirem)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
