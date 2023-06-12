import logging
import re
from typing import Optional

from service.replaceToken import replace_env_variable
from utils.file_utils import *


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


def apply_config(input_file, query, output_file):

    #todo validate inputs

    queries = Query(**query)

    file_properties = []

    for line in input_file:
        new_line = line
        match = re.search(r'^[^#]\s*(\w+(\.\w+)+|\w+)\s*=\s*', line)
        if match:
            property = match.group().replace("=", "")
            property = property.strip()
            file_properties.append(property)

            for updateQuery in queries.update:
                if property == updateQuery.update:
                    print(f"Update property: {property}")
                    print(f"Old value: {line}")
                    new_line = updateQuery.update + "=" + updateQuery.value + "\n"
                    print(f"New value: {new_line}")

        output_file.write(new_line)

    if len(queries.insert)>0:
        output_file.write("\n# ===== Properties above this line were generated based on custom configuration ======\n\n")
        for insertQuery in queries.insert:
            if not insertQuery.insert in file_properties:
                print(f"Insert property: {insertQuery.insert}={insertQuery.value}")
                if insertQuery.comment:
                    output_file.write("\n# " + insertQuery.comment + "\n")
                output_file.write(insertQuery.insert + "=" + insertQuery.value + "\n")
                file_properties.append(insertQuery.insert)
            else:
                logging.warning(f"Failed to insert: Property [{insertQuery.insert}] already exists.")

    return output_file
