# user/utils.py

# утилиты необходимые для работы данного пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os
from flask import current_app
from wtforms.validators import ValidationError

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class FileSize:
    '''Проверяет размер загружаемого файла'''
    def __init__(self, max=None, message=None):
        self.message = message
        self.max = max

    def __call__(self, form, field):
        config_max = current_app.config['MAX_CONTENT_LENGTH']
        data = field.data
        message = self.message


        if self.max is None:
            self.max = config_max

        if self.max > config_max:
            config_max = self.max

        if data is not None:
            if os.fstat(data.fileno()).st_size > self.max:
                print(os.fstat(data.fileno()).st_size, self.max)
                if self.message is None:
                    message = field.gettext('Max size {}'.format(size))

                raise ValidationError(message)