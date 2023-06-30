from typing import Optional
from service.replaceToken import replace_env_variable


class Query:
    delete = []
    update = []
    insert = []
    def __init__(self, **query):
        if 'delete' in query:
            self.delete = []
            for dlt in query['delete']:
                self.delete.append(DeleteQuery(**dlt))

        if 'update' in query:
            self.update = []
            for upd in query['update']:
                self.update.append(UpdateQuery(**upd))

        if 'insert' in query:
            self.insert = []
            for ins in query['insert']:
                self.insert.append(InsertQuery(**ins))


class DeleteQuery:
    delete: str
    element: str
    where: Optional[str] = None
    def __init__(self, **query):
        self.delete = replace_env_variable(query['delete'])
        self.element = replace_env_variable(query['element'])
        if 'where' in query:
            self.where = replace_env_variable(query['where'])


class UpdateQuery:
    update: str
    element: str
    value: str
    where: Optional[str] = None
    def __init__(self, **query):

        assert query['update'] is not None
        assert query['element'] is not None
        assert query['value'] is not None
        
        self.update = replace_env_variable(query['update'])
        self.element = query['element']
        self.value = replace_env_variable(query['value'])
        if 'where' in query:
            self.where = replace_env_variable(query['where'])


class InsertQuery:
    insert: str
    element: Optional[str] = None
    attribute: Optional[str] = None
    def __init__(self, **query):
        
        assert query['insert'] is not None
        
        self.insert = replace_env_variable(query['insert'])
        if 'element' in query:
            self.element = replace_env_variable(query['element'])
        if 'attribute' in query:
            if 'name' in query['attribute']:
                query['attribute']['name'] = replace_env_variable(query['attribute']['name'])
            if 'value' in query['attribute']:
                query['attribute']['value'] = replace_env_variable(query['attribute']['value'])
            self.attribute = query['attribute']