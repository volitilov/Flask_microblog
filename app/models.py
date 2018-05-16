# app/models.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime

from flask import current_app

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db, login_manager

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Role(db.Model):
    '''Создаёт роли для пользователей'''
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

    def __str__(self):
        return '<Role - {}>'.format(self.name)


class User(UserMixin, db.Model):
    '''Создаёт пользователей'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    location = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    date_registration = db.Column(db.DateTime(), default=datetime.utcnow()) 
    last_visit = db.Column(db.DateTime(), default=datetime.utcnow())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            else:
                self.role = Role.query.filter_by(name='User').first()

    def generate_confirmation_token(self, expiration=3600):
        '''Генерирует маркер со сроком хранения (по умолчанию на один час)
        для потверждения акаунта'''
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({ 'confirm': self.id }).decode('utf-8')


    def generate_resetPassword_token(self, expiration=3600):
        '''Генерирует маркер со сроком хранения (по умолчанию на один час)
            для сброса пароля'''
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({ 'reset': self.id }).decode('utf-8')
    

    def generate_changeEmail_token(self, new_email, expiration=3600):
        '''Генерирует маркер со сроком хранения (по умолчанию на один час)
            для изминения email'''
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({ 'change_email': self.id, 'new_email': new_email }).decode('utf-8')


    @property
    def password(self):
        '''Закрывает доступ на чтение пароля'''
        raise AttributeError('пароль не является читаемым атрибутом')


    @password.setter
    def password(self, password):
        '''Генерирует хеш из пароля'''
        self.password_hash = generate_password_hash(password)


    @staticmethod
    def reset_password(token, new_password):
        '''Проверяет если токен верен, записывает новый пароль'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True


    def verify_password(self, password):
        '''Сравнивает пполученный пароль с захешированным паролем 
        лежащим в базе данных'''
        return check_password_hash(self.password_hash, password)


    def confirm(self, token):
        '''Проверяет маркер и, если ошибок не обнаруженно, записывает в новый
        атрибут "confirmed" значение True.
        Помимо проверки маркера, функции "confirm" проверяет также соответствие
        "id" из маркера с числовым индетификатором аутентифицировавшегося 
        пользователя, хранящимся в переменной "current_user".
        Это гарантирует, что даже если злоумышленик узнает, как генерируются 
        маркеры, он не сможет подтвердить чужую учетную запись.'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def change_email(self, token):
        '''Проверяет токен и если всё впорядке, то изменяет email текущего
	    пользователя.'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True


    def is_admin(self):
        '''Проверяет является ли текущий пользователь администратором.'''
        if self.email == current_app.config['FLASKY_ADMIN']:
            return True
        return False


    def ping(self):
        self.last_visit = datetime.utcnow()
        db.session.add(self)


    def __str__(self):
        return '<User - {}>'.format(self.name)





class Post(db.Model):
    '''Создаёт статьи'''
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    text = db.Column(db.Text)





@login_manager.user_loader
def load_user(user_id):
    '''Принимает идентификатор в виде строки Юникода и, если указанный 
    идентификатор существует, возвращает объект, представляющий пользователя, 
    в противном случае возвращается None''' 
    return User.query.get(int(user_id))
