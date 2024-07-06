import json
import os
from datetime import datetime
from sqlite3 import IntegrityError
from urllib.parse import unquote

from flask import redirect, jsonify, url_for, request
from flask_openapi3 import Info, OpenAPI, Tag

from config import Config
from flask_sqlalchemy import SQLAlchemy
from database import create_database, Session
from flask_cors import CORS

from models.produto import Produto
from models.usuario import User
from schemas.error import ErrorSchema
from schemas.produto import ProdutoSchema, ProdutoListSchema, DeleteProdutoSchema, ProdutoQuerySchema
from schemas.usuario import UserSchema, UserListSchema
from werkzeug.utils import secure_filename

info = Info(title='Brechó TendTudo', version='1.0.0')

app = OpenAPI(__name__, info=info)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)

usuario_tag = Tag(name='Usuários', title='Usuario', description='CRUD de Usuários')
produto_tag = Tag(name='Produtos', title='Produtos', description='CRUD de Produtos')


# When you define the path
@app.get("/")
def api_home():
    return redirect('/openapi')


@app.get("/usuario", tags=[usuario_tag], responses={"200": UserListSchema, "400": ErrorSchema})
def get_users():
    session = Session()
    usuarios = session.query(User).all()

    usuario_json = []
    for usuario in usuarios:
        usuario_json.append({
            "id": usuario.id,
            "username": usuario.username,
            "email": usuario.email
        })

    return {"usuarios": usuario_json}


@app.post("/usuarios", tags=[usuario_tag], responses={"200": UserSchema, "400": ErrorSchema})
def create_user(form: UserSchema):
    usuario = User(
        username=form.username,
        email=form.email)
    try:
        session = Session()
        session.add(usuario)
        session.commit()
        return jsonify(usuario)

    except IntegrityError as e:
        err_message = f'Não foi possível salvar o usuário. O nome selecionado já existe na base de dados.'
        return {"message": err_message}, 400
    except Exception as e:
        err_message = f'Não foi possível adicionar o usuário. Tente novamente.'
        return {"message": err_message}, 400


@app.get("/produto", tags=[produto_tag], responses={"200": ProdutoListSchema, "400": ErrorSchema, "500": ErrorSchema})
def get_produtos():
    session = Session()
    produtos_query = session.query(Produto).all()

    produtos_list = []
    for produto in produtos_query:
        produtos_list.append({"id": produto.id, "descricao": produto.descricao, "preco_venda": produto.preco_venda,
                              "preco_custo": produto.preco_custo,
                              "data_criacao": produto.data_criacao.strftime('%Y-%m-%d'), "is_novo": produto.is_novo})
                              # "imagem": url_for('static', filename=produto.imagem)})

    return {"produtos": produtos_list}


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/produto", tags=[produto_tag], responses={"200": ProdutoSchema, "400": ErrorSchema})
def create_produto(form: ProdutoSchema):
    print(request.files)
    # if 'imagem' not in request.files:
    #     return jsonify({"err_message": "Você precisa informar uma imagem para o produto."}), 400

    # file = request.files['imagem']
    #
    # if file.filename == '':
    #     return jsonify({"message": "Nenhuma imagem selecionada. Tente novamente."}), 400

    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     file.save(file_path)

    produto = Produto(descricao=form.descricao,
                      preco_venda=form.preco_venda,
                      preco_custo=form.preco_custo,
                      data_criacao=datetime.now(),
                      is_novo=bool(form.is_novo),
                      imagem=None)
    try:
        session = Session()
        session.add(produto)
        session.commit()
        return produto.to_dict(), 200
    except Exception as e:
        err_message = f'{e.args}'
        return {"message": err_message}, 400

# else:
# return jsonify({"error": "Allowed image types are -> png, jpg, jpeg, gif"}), 400


@app.delete('/produto', tags=[produto_tag],
            responses={"200": DeleteProdutoSchema, "404": ErrorSchema})
def delete_produto(query: ProdutoQuerySchema):
    print('id que chegou no back: ', query.id)
    session = Session()
    count = session.query(Produto).filter(Produto.id == query.id).delete()
    session.commit()

    if count:
        return {"message": "Produto removido", "id": query.id}
    else:
        err_msg = "Produto não encontrado na base :/"
        return {"mesage": err_msg}, 404


if __name__ == '__main__':
    app.run()
