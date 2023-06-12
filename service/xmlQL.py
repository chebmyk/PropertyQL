import logging
from typing import Optional

from lxml import etree
from service.replaceToken import replace_env_variable
from utils.file_utils import *
from utils.xml_utils import *


class InsertQuery:
    insert: str
    element: Optional[str] = None
    attribute: Optional[str] = None
    def __init__(self, **entries):
        self.insert = replace_env_variable(entries['insert'])
        if 'element' in entries:
            self.element = replace_env_variable(entries['element'])
        if 'attribute' in entries:
            if 'name' in entries['attribute']:
                entries['attribute']['name'] = replace_env_variable(entries['attribute']['name'])
            if 'value' in entries['attribute']:
                entries['attribute']['value'] = replace_env_variable(entries['attribute']['value'])
            self.attribute = entries['attribute']


class UpdateQuery:
    update: str
    field: str
    value: str
    where: str
    def __init__(self, **entries):
        self.update = replace_env_variable(entries['update'])
        self.field = entries['field']
        self.value = replace_env_variable(entries['value'])
        self.where = replace_env_variable(entries['where'])


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


def apply_config(xml_tree, query):

    #todo validate inputs

    queries = None

    queries = Query(**query)

    for updateQuery in queries.update:

        entry = list(filter(lambda elem: len(elem.xpath(updateQuery.where)) > 0, xml_tree.xpath(f"{updateQuery.update}")))
        if len(entry) == 1 :
            print(f"Update Object: {etree.tostring(entry[0])}")

            field = entry[0].xpath(updateQuery.field)
            if field:
                field = field[0]
                if isinstance(field, elTree._Element):
                    print(f"Old value: {etree.tostring(field)}")
                    field.text = updateQuery.value
                    print(f"New value: {etree.tostring(field)}")
                else:
                    print(f"Old value: {etree.tostring(field.getparent())}")
                    field.getparent().set(field.attrname, updateQuery.value)
                    print(f"New value: {etree.tostring(field.getparent())}")
            else:
                logging.warning(f"Updated field [{updateQuery.field}] doesn't exists")

        elif len(entry) == 0 :
            logging.warning("No Records found for update")
            logging.warning(f"{etree.tostring(updateQuery.update)}[{etree.tostring(updateQuery.where)}]")
        else:
            logging.error(f"Incorrect update query. Multiple update is not supported. {etree.tostring(updateQuery.update)}[{etree.tostring(updateQuery.where)}]")
            raise Exception("Error occurred while running update stmt")


    for insertQuery in queries.insert:
        entry = xml_tree.xpath(f"{insertQuery.insert}")
        if len(entry) == 1:
            targetElement = entry[0]
            if insertQuery.element:
                print(f"insert into {xml_tree.getpath(targetElement)}")
                newElement = etree.fromstring(insertQuery.element)

                if check_duplicates(targetElement, newElement):
                    raise Exception(f"Error: Item already exists. {etree.tostring(newElement)} ")

                targetElement.append(newElement)
                print(f"value ({etree.tostring(newElement)})")
            elif insertQuery.attribute:
                print(f"insert into {xml_tree.getpath(targetElement)}")
                print(f"attribute:{insertQuery.attribute['name']} value:{insertQuery.attribute['value']}")
                targetElement.set(insertQuery.attribute['name'], insertQuery.attribute['value'])
                print(f"value ({etree.tostring(targetElement)})")
        elif len(entry) == 0:
            logging.warning(f"Warning: Target Element not found {etree.tostring(insertQuery.insert)}")
        else:
            logging.error(f"Incorrect Insert query. You are trying to insert into multiple tags. Please check insert statement {etree.tostring(insertQuery.insert)}")
            raise Exception("Error: occurred while running insert stmt")

    #pretty_xml = etree.tostring(xml_tree.getroot(), pretty_print=True)
    return xml_prettify(xml_tree)
