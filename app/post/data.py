# post/data.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_login import current_user

from ..models.post import Post


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def get_posts():
    return {
        'all_posts': Post.query.filter_by(moderation=True),
        'followed_posts': current_user.followed_posts.filter(Post.moderation==True)
    }


page_titles = {
    'posts_page': 'Cтраница со всеми публикациями.',
    'followedPosts_page': 'Публикации по подписке',
    'addPost_page': 'Страница добавления поста.',
    'userPosts_page': 'Страница с публикациями пользователя.',
    'tagPosts_page': 'Страница с публикациями по запрошенному тегу.',
    'post_page': 'Пост - ',
    'editPost_page': 'Страница редактирования поста',
    'byViewingPosts_page': 'Публикации по кол-ву просмотров.',
    'byRatingPosts_page': 'Публикации по рейтингу.'
}