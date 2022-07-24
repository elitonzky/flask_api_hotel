from lib2to3.pgen2 import token
import traceback
from flask import make_response
from flask_restful import Resource, reqparse
from models.usuario import UserModel 
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, get_jwt
from blacklist import BLACKLIST
from flask import make_response, render_template

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="Login cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="Senha cannot be left blank")
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool)


class User(Resource):
    # /usuario/user_id
    def get(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
            return {'message': f'{user.json()}'}, 200 # Success
        return {'message': 'User not found'}, 404 # not found
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred trying to delete usuer.'}, 500 # internal server error
            return {'message': f'User #{user.json()} has ben deleted'}, 200 # success
        return {'message': f'User #{user_id} not found'}, 404 # Not Found


class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        login = dados['login']
        email = dados['email']
        
        if not email or email is None:
            return {'message': 'The field email cannot be left blank.'}, 400
        
        if UserModel.find_by_email(email):
            return {'message': f'The email {email} already exists.'}, 400

        if UserModel.find_by_login(login):
            return {'message': f'The login {login} already exists'}

        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'Internal server error has ocurred.'}, 500 # Internal server error
        
        return {'message': 'user created sucessfully'}, 201 # Created


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UserModel.find_by_login(dados['login'])
        
        if user and safe_str_cmp(user.senha,dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'acess_token': token_de_acesso}, 200
            return {'message': 'User not confirmed'}, 400
        return {'message': 'The username or passwaord is incorrect'}, 401 # unauthorize
 
    
class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
    

class UserConfirm(Resource):
    # raiz/confirmacao/{user_id}
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_user(user_id)
            
        if not user:
            return {'message': f'user {user_id} not found'}, 404
        
        user.ativado= True 
        user.save_user()
        #return {'message': f'user id {user_id} confirmed succesfuly'}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login), 200)