# main/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, jsonify

from .. import (
    # blueprint
    main,

    # forms
    Search_form,

    # utils
    flash_errors
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/posts/...search', methods=['POST'])
def searchForm_req():
    form = Search_form()

    if form.validate():
        return jsonify({
            'next_url': url_for('main.searchResults_page', data=form.q.data)
        })
        
    return jsonify({'errors': flash_errors(form)})

    