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

@notice.route('/notice/<int:id>/...del', methods=['POST'])
@login_required
def deleteNotice_request(id):
    notice = Notice.query.get_or_404(id)
   
    if current_user != notice.author:
        abort(403)

    db.session.delete(notice)
    db.session.commit()
    
    return jsonify({'success': True})
