from sql_alchemy import banco
from flask import request,url_for
from requests import post 

MAILGUN_DOMAIN = 'sandbox04344fe1a0ab4670b5eacbe1d609f03a.mailgun.org'
MAILGUN_API_KEY = 'ff751135b6ff4e7f29d36acd4c17e400-787e6567-ebfefb6d'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@restapi.com'



class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, ativado, email):
        self.login = login
        self.senha = senha
        self.ativado = ativado
        self.email = email

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id) 
        envio = post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE}<{FROM_EMAIL}>',
                          'to': self.email,
                          'subject': 'Confirmação de Cadastro',
                          'text': f'Confirme seu cadastro clicando no link a seguir:{link}',
                          'html': f'<html><p> Confirme seu cadastro clicando no link a seguir: <a href="{link}"> Confirmar EMAIL</a> </p> </html>'}
                    )
        return envio
        
    
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
        
