from flask import request, jsonify
from models import db, Usuario, Conversa
import bcrypt

def initialize_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        usuario_existente = Usuario.query.filter_by(email=data['email']).first()
        if usuario_existente:
            return jsonify({"message": "E-mail já cadastrado!"}), 400

        senha_hash = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())
        usuario = Usuario(
            nome=data['nome'],
            email=data['email'],
            senha=senha_hash.decode('utf-8')
        )
        db.session.add(usuario)
        db.session.commit()
        return jsonify({"message": "Usuário registrado com sucesso!"}), 201

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

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        usuario_id = data['usuario_id']
        mensagem = data['mensagem']
        resposta_bot = "Olá! Esta é uma mensagem de autoajuda."

        conversa = Conversa(
            usuario_id=usuario_id,
            mensagem_usuario=mensagem,
            mensagem_bot=resposta_bot
        )
        db.session.add(conversa)
        db.session.commit()
        return jsonify({"resposta": resposta_bot}), 200
