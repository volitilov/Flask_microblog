# notice/routes/reqs.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import flash, jsonify
from flask_login import current_user, login_required

from .. import (
    # blueprint
    notice,

    # models
    Notice,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@notice.route('/<username>/notice/<int:id>/...del', methods=['POST'])
@login_required
def deleteNotice_request(username, id):
    notice = Notice.query.get_or_404(id)
   
    if current_user == notice.author:
        db.session.delete(notice)
        db.session.commit()
    else:
        flash(category='warn', 
            message='Вы не можите удалить уведомление, так как не являетесь его владельцом')
        return jsonify({
            'success': False
        })
    
    return jsonify({
        'success': True
    })
