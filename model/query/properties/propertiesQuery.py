from typing import Optional
from service.replaceToken import replace_env_variable


class Query:
    update = []
    insert = []
    def __init__(self, **entries):
        if 'update' in entries:
            self.update = []
            for upd in entries['update']:
                self.update.append(UpdateQuery(**upd))
        if 'insert' in entries:
            self.insert = []
            for ins in entries['insert']:
                self.insert.append(InsertQuery(**ins))


class InsertQuery:
    insert: str
    value: str
    comment: Optional[str] = None
    def __init__(self, **entries):
        self.insert = entries['insert']
        self.value = replace_env_variable(entries['value'])
        if 'comment' in entries:
            self.comment = entries['comment']


class UpdateQuery:
    update: str
    value: str
    def __init__(self, **entries):
        self.update = entries['update']
        self.value = replace_env_variable(entries['value'])



