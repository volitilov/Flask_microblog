# app/models/user.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from markdown2 import markdown
import bleach
import jwt
from time import time

from datetime import datetime
from hashlib import md5

from flask import current_app, url_for

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .role import Role
from .post import Post
from .message import Message
from .. import db, login_manager

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())



class User(UserMixin, db.Model):
    '''Создаёт пользователей'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    about_me = db.Column(db.Text, nullable=True)
    about_me_html = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    writer = db.Column(db.Boolean, default=False)
    date_registration = db.Column(db.DateTime, default=datetime.utcnow()) 
    last_visit = db.Column(db.DateTime, default=datetime.utcnow())
    avatar_hash = db.Column(db.String(32))
    photo_url = db.Column(db.String, nullable=True)
    rating = db.Column(db.Integer, index=True, default=0)

    settings = db.relationship('UserSettings', backref='profile', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    post_ratings = db.relationship('Post_rating', backref='author', lazy='dynamic')
    notice = db.relationship('Notice', backref='author', lazy='dynamic')

    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                    backref='recipient', lazy='dynamic')
    
    followed = db.relationship('Follow', foreign_keys=[Follow.followed_id],
            backref=db.backref('follower', lazy='joined'),
            lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.follower_id],
            backref=db.backref('followed', lazy='joined'),
            lazy='dynamic', cascade='all, delete-orphan')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.follow(self)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = md5(self.email.encode('utf-8')).hexdigest()

        if self.role is None:
            if self.email == current_app.config['APP_ADMIN']:
                if Role.query.filter_by(name='Admin').first() is None:
                    self.role = Role(name='Admin')
                else:
                    self.role = Role.query.filter_by(name='Admin').first()
            elif self.email == current_app.config['APP_MODERATOR']:
                if Role.query.filter_by(name='Moderator').first() is None:
                    self.role = Role(name='Moderator')
                else:
                    self.role = Role.query.filter_by(name='Admin').first()
            else:
                if Role.query.filter_by(name='User').first() is None:
                    self.role = Role(name='User')
                else:
                    self.role = Role.query.filter_by(name='User').first()


    def generate_confirmation_token(self, expiration=3600):
        '''Генерирует маркер со сроком хранения (по умолчанию на один час)
        для потверждения акаунта'''
        return jwt.encode(
            payload={ 'confirm': self.id, 'exp': time()+expiration }, 
            key=current_app.config['SECRET_KEY'])


    def generate_resetPassword_token(self, expiration=3600):
        '''Генерирует маркер со сроком хранения (по умолчанию на один час)
        для сброса пароля'''
        return jwt.encode(
            payload={ 'reset': self.id, 'exp': time()+expiration },
            key=current_app.config['SECRET_KEY'])
    

    def generate_changeEmail_token(self, new_email, expiration=3600):
        '''Генерирует маркер со сроком хранения (по умолчанию на один час)
            для изминения email'''
        return jwt.encode(
            payload={ 
                'reset': self.id, 
                'change_email': self.id, 
                'new_email': new_email,
                'exp': time()+expiration },
            key=current_app.config['SECRET_KEY'])


    def generate_auth_token(self, expiration):
        return jwt.encode(
            payload={ 'reset': self.id, 'exp': time()+expiration },
            key=current_app.config['SECRET_KEY'])
    

    @property
    def password(self):
        '''Закрывает доступ на чтение пароля'''
        raise AttributeError('пароль не является читаемым атрибутом')


    @password.setter
    def password(self, password):
        '''Генерирует хеш из пароля'''
        self.password_hash = generate_password_hash(password)


    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.follower_id==Post.author_id) \
            .filter(Follow.followed_id==self.id)


    @staticmethod
    def reset_password(token, new_password):
        '''Проверяет если токен верен, записывает новый пароль'''
        try:
            data = jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'])
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True


    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'])
        except:
            return None
        return User.query.get(data['id'])


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
        try:
            data = jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'])
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
        try:
            data = jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'])
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
        self.avatar_hash = md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    
    @property
    def is_admin(self):
        '''Проверяет является ли текущий пользователь администратором.'''
        if self.email == current_app.config['APP_ADMIN']:
            return True
        return False
    
    
    @property
    def is_moderator(self):
        '''Проверяет является ли текущий пользователь модератором.'''
        if self.email == current_app.config['APP_MODERATOR']:
            return True
        return False


    def ping(self):
        '''Фиксирует текущее время для свойства пользователя 
        (последнее посещение)'''
        self.last_visit = datetime.utcnow()
        db.session.add(self)


    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://ru.gravatar.com/avatar'
        hash = self.avatar_hash or md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,
                hash=hash, size=size, default=default, rating=rating)


    def follow(self, user):
        '''Реализует подписку на пользователя.'''
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)
            db.session.commit()


    def unfollow(self, user):
        '''Реализует отписку от пользователя на кототорого подписан.'''
        f = self.followed.filter_by(follower_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    
    def is_following(self, user):
        '''Возвращает True если текущий пользователь подписан на 
        запрашиваемого пользователя.'''
        if user.id is None:
            return False
        if self.followed.filter_by(follower_id=user.id).first() is not None:
            return True


    def is_followed_by(self, user):
        '''Вернёт True если запрашиваемый пользователь подписан на текущего.'''
        if user.id is None:
            return False
        if self.followers.filter_by(followed_id=user.id).first() is not None:
            return True


    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'about': self.about_me,
            'location': self.location,
            'date_registration': self.date_registration,
            'last_visit': self.last_visit,
            'posts_url': url_for('api.get_userPosts', id=self.id),
            'followed_posts_url': url_for('api.get_userFollowedPosts', id=self.id),
            'post_count': self.posts.count()
        }
        return json_user


    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''Функция создаёт HTML-версию данных пользователя "обо мне" и 
        сохраняет его в поле body_html, обеспечивая тем самым автоматическое 
        преобразование разметки Markdown в html'''
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'i', 'li', 'ol', 
            'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img', 'br', 
            'table', 'tbody', 'thead', 'td', 'th', 'tr']

        allowed_attrs = ['href', 'rel', 'alt', 'title', 'style', 'width', 'height', 
            'src', 'target', 'id']
        allowed_style = ['color', 'width', 'height']
        allowed_protocols=['http', 'https']
        
        target.about_me_html = bleach.linkify(bleach.clean(
            markdown(value, extras=[
                    'break-on-newline', 'cuddled-lists', 'footnotes', 'nofollow', 
                    'numbering', 'tables', 'wiki-tables']),
                attributes=allowed_attrs, tags=allowed_tags, 
                styles=allowed_style, protocols=allowed_protocols, 
                strip=True))


    def __repr__(self):
        return '<User - {}>'.format(self.name)




@login_manager.user_loader
def load_user(user_id):
    '''Принимает идентификатор в виде строки Юникода и, если указанный 
    идентификатор существует, возвращает объект, представляющий пользователя, 
    в противном случае возвращается None''' 
    return User.query.get(int(user_id))



db.event.listen(User.about_me, 'set', User.on_changed_body)