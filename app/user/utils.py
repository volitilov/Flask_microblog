# user/utils.py

# утилиты необходимые для работы данного пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os
from functools import wraps

from flask import current_app
from flask_login import current_user
from wtforms.validators import ValidationError
from werkzeug.exceptions import RequestEntityTooLarge

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class FileSize:
    '''Проверяет размер загружаемого файла'''
    def __init__(self, max=None, message=None):
        self.message = message
        self.max = max

    def __call__(self, form, field):
        data = field.data
        message = self.message

        if self.max is None:
            self.max = current_app.config['MAX_CONTENT_LENGTH']

        if self.max is not None and data is not None:
            if os.fstat(data.fileno()).st_size > self.max:
                if self.message is None:
                    message = field.gettext('Max size {}'.format(size))

                raise ValidationError(message)
