# moderator/data.py

# формирует данные для роутов

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import current_app 

from . import Post, Comment, User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def get_data():
    moderator = current_app.config['APP_MODERATOR']
    user = User.query.filter_by(email=moderator).first()

    comments = Comment.query.filter_by(state='moderation')
    posts = Post.query.filter_by(state='moderation')
            
    return {
        'posts': posts,
        'comments': comments,
        'messages': user.messages_received
    }


page_titles = {
    'dashboard_page': 'Страница модератора.',
    'posts_page': 'Страница публикации для модерации',
    'post_page': 'Страница публикации',
    'returnPost_page': 'Страница формы уведомления',
    'messages_page': 'Страница сообщений службы поддержки'
}