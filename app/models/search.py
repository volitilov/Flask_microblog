# app/models/search.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .. import db
from ..search import add_to_index, remove_from_index, query_index

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class SearchableMixin:
    @classmethod
    def search(cls, expression, page, per_page):
        '''Возвращает запрос, который заменяет список идентификаторов объектов 
        на фактические объекты, а также передает общее количество результатов 
        поиска в качестве второго возвращаемого значения.'''
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        when = []
        if total == 0:
            return cls.query.filter_by(id=0), 0
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total
    

    @classmethod
    def before_commit(cls, session):
        '''Хронит объекты которые будут добавлены, изменены или удалены. Как 
        только сеанс пофиксится они будут использоваться для обновления индекса 
        Elasticsearch'''
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }
    

    @classmethod
    def after_commit(cls, session):
        '''Вносит изменения на стороне Elasticsearch. Объект сеанса имеет 
        переменную _changes, которая добавлена в before_commit(), поэтому теперь 
        можно перебирать добавленные, измененные и удаленные объекты и выполнять 
        соответствующие вызовы для функций индексирования в app/search.py.'''
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None


    @classmethod
    def reindex(cls):
        '''Вспомогательный метод, который используется для обновления индекса 
        со всеми данными из реляционной стороны'''
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)



