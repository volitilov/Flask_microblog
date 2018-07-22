# comment/data.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from ..models.post import Post
from ..models.comment import Comment

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def get_data(current_user, user):
    posts = user.posts.filter_by(state='public')
    comments = user.comments.filter_by(state='public')
    if not current_user.is_anonymous:
        if current_user == user:
            posts = user.posts.filter(Post.state!='moderation')
            comments = user.comments.filter(Comment.state!='moderation')
            
    return {
        'posts': posts,
        'comments': comments
    }



page_titles = {
    'addComment_page': 'Страница добавления комментария',
    'comments_page': 'Страница с комментариями пользователя.',
    'comment_page': 'Страница комментария',
    'editComment_page': 'Страница редактирования коментария'
}