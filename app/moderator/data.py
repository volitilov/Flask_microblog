# moderator/data.py

# формирует данные для роутов

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from . import Post, Comment

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def get_data():
    comments = Comment.query.filter_by(state='moderation')
    posts = Post.query.filter_by(state='moderation')
            
    return {
        'posts': posts,
        'comments': comments
    }


page_titles = {
    'dashboard_page': 'Страница модератора.',
    'posts_page': 'Страница публикации для модерации',
    'post_page': 'Страница публикации',
    'returnPost_page': 'Страница формы уведомления'
}