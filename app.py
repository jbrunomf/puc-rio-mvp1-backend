import json
from sqlite3 import IntegrityError
from typing import List

from flask import redirect, jsonify
from flask_openapi3 import Info, OpenAPI, Tag

from config import Config
from flask_sqlalchemy import SQLAlchemy
from database import create_database, Session
from flask_cors import CORS
from sqlalchemy import select

from models.user import User
from schemas.error import ErrorSchema
from schemas.user import UserSchema, UserListSchema

info = Info(title='Brechó TendTudo', version='1.0.0')

app = OpenAPI(__name__, info=info)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)

usuario_tag = Tag(name='Usuários', title='Usuario', description='CRUD de usuários')


# When you define the path
@app.get("/")
def api_home():
    return redirect('/openapi')


@app.get("/users", tags=[usuario_tag], responses={"200": UserListSchema, "400": ErrorSchema})
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


@app.post("/users", tags=[usuario_tag], responses={"200": UserSchema, "400": ErrorSchema})
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
        err_message = f'Não foi psossível salvar o usuário. O nome selecionado já existe na base.'
    except Exception as e:
        err_message = f'Não foi possível adicionar o usuário. Tente novamente.'
        return {"message": err_message}, 400


if __name__ == '__main__':
    app.run()
