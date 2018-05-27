# app/utils.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from random import randint

from flask import make_response, render_template, request
from sqlalchemy.exc import IntegrityError
import forgery_py as forgery

from . import db
from .models.post import Post
from .models.user import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def create_response(template, data):
	'''Делает обёртку для объекта ответа.'''
	resp = make_response(render_template(template, data=data))
	resp.delete_cookie('next')
	if request.args.get('next') is not None: 
		resp.set_cookie(key='next', value=request.args.get('next'))
	return resp



def generate_fake_posts(count=100):
	'''Генерирует фейковые посты в заданном кол-ве.'''
	user_count = User.query.count()
	for i in range(count):
		u = User.query.offset(randint(0, user_count - 1)).first()
		p = Post(title=forgery.lorem_ipsum.title(),
				text=forgery.lorem_ipsum.sentences(randint(1, 4)),
				author=u,
				data_creation=forgery.date.date(True))
		db.session.add(p)
		db.session.commit()



def generate_fake(count=100):
	'''Генерирует фейковых пользователей в заданном кол-ве.'''
	i = 0
	while i < count:
		u = User(email=forgery.internet.email_address(),
			name=forgery.internet.user_name(True),
			password=forgery.lorem_ipsum.word(),
			confirmed=True,
			first_name=forgery.name.first_name(),
			last_name=forgery.name.last_name(),
			location=forgery.address.country(),
			about_me=forgery.lorem_ipsum.sentence(),
			date_registration=forgery.date.date(True))
		db.session.add(u)
		try:
			db.session.commit()
			i +=1
		except IntegrityError:
			db.session.rollback()



def add_self_follows():
	'''Регестрация существующих пользователей как читающих
	самих себя.'''
	for user in User.query.all():
		if not user.is_following(user):
			user.follow(user)
			db.session.add(user)
			db.session.commit()

