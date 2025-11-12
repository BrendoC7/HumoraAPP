from flask import request, jsonify
from models import db, Usuario, Conversa, Emocao
import bcrypt
import re 
from datetime import datetime, date
import pytz

def initialize_routes(app):

    # REGISTRO
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()

        # Validação de e-mail usando regex
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, data.get('email', '')):
            return jsonify({"message": "E-mail inválido!"}), 400

        # Verifica se o e-mail já existe
        usuario_existente = Usuario.query.filter_by(email=data['email']).first()
        if usuario_existente:
            return jsonify({"message": "E-mail já cadastrado!"}), 400

        # Criação da senha hash
        senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        usuario = Usuario(
            nome=data['nome'],
            email=data['email'],
            senha=senha_hash.decode('utf-8')
        )

        # Salva no banco
        db.session.add(usuario)
        db.session.commit()

        return jsonify({"message": "Usuário registrado com sucesso!"}), 201
    # LOGIN
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        usuario = Usuario.query.filter_by(email=data['email']).first()

        if not usuario:
            return jsonify({"message": "E-mail não encontrado!"}), 404

        if not bcrypt.checkpw(data['senha'].encode('utf-8'), usuario.senha.encode('utf-8')):
            return jsonify({"message": "Senha incorreta!"}), 401

        return jsonify({
            "message": "Login bem-sucedido!",
            "usuario_id": usuario.id
        }), 200


    # CHAT
    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        usuario_id = data['usuario_id']
        mensagem = data['mensagem']
        resposta_bot = "Olá! Esta é uma mensagem automática de resposta."

        conversa = Conversa(
            usuario_id=usuario_id,
            mensagem_usuario=mensagem,
            mensagem_bot=resposta_bot
        )

        db.session.add(conversa)
        db.session.commit()

        return jsonify({"resposta": resposta_bot}), 200

    @app.route('/emocao', methods=['POST'])
    def registrar_emocao():
        data = request.get_json()

        if 'usuario_id' not in data or 'tipo' not in data:
            return jsonify({"message": "Campos obrigatórios faltando!"}), 400

        usuario_id = data['usuario_id']

        # Verifica se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"message": "Usuário não encontrado!"}), 404

        # Checa se já existe uma emoção registrada hoje (horário de Brasília)
        brt = pytz.timezone('America/Sao_Paulo')
        hoje_brt = datetime.now(brt).date()

        emocao_existente = Emocao.query.filter(
            Emocao.usuario_id == usuario_id,
            db.func.date(Emocao.data_criacao) == hoje_brt
        ).first()

        if emocao_existente:
            return jsonify({"message": "Você já registrou uma emoção hoje!"}), 400

        # Cria a emoção
        emocao = Emocao(
            usuario_id=usuario_id,
            tipo=data['tipo'],
            intensidade=data.get('intensidade'),
            observacao=data.get('observacao'),
            data_criacao=datetime.now(brt)  # define horário de criação no BRT
        )

        db.session.add(emocao)
        db.session.commit()

        return jsonify({
            "message": "Emoção registrada com sucesso!",
            "data_criacao": emocao.data_criacao.isoformat()
        }), 201
