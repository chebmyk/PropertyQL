import logging
from typing import Optional
from lxml import etree
from service.replaceToken import replace_env_variable
from utils.file_utils import *
from utils.xml_utils import *


class DeleteQuery:
    delete: str
    element: str
    where: Optional[str] = None
    def __init__(self, **entries):
        self.delete = replace_env_variable(entries['delete'])
        self.element = replace_env_variable(entries['element'])
        if 'where' in entries:
            self.where = replace_env_variable(entries['where'])


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
    where: Optional[str] = None
    def __init__(self, **entries):
        self.update = replace_env_variable(entries['update'])
        self.field = entries['field']
        self.value = replace_env_variable(entries['value'])
        if 'where' in entries:
            self.where = replace_env_variable(entries['where'])


class Query:
    delete = []
    update = []
    insert = []
    def __init__(self, **entries):
        if 'delete' in entries:
            self.delete = []
            for dlt in entries['delete']:
                self.delete.append(DeleteQuery(**dlt))

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

    queries = Query(**query)

    for deleteQuery in queries.delete:
        entry = []

        if deleteQuery.where:
            entry = list(filter(lambda elem: len(elem.xpath(deleteQuery.where)) > 0, xml_tree.xpath(f"{deleteQuery.delete}")))
        else:
            entry = xml_tree.xpath(f"{deleteQuery.delete}")

        if len(entry) == 1 :
            print(f"Delete from Object: {etree.tostring(entry[0])}")
            found = entry[0].xpath(deleteQuery.element)
            if found:
                element = found[0]
                if isinstance(element, elTree._Element):
                    print(f"Element: {element.tag}")
                    element.getparent().remove(element)
                else:
                    start = deleteQuery.element.rindex("@")
                    attribute_name = deleteQuery.element[start+1:]
                    print(f"Attribute: {attribute_name}")
                    element.getparent().attrib.pop(attribute_name, None)
            else:
                logging.warning(f"Updated field [{deleteQuery.element}] doesn't exists")

        elif len(entry) == 0 :
            logging.warning("No Records found to delete")
            logging.warning(f"{deleteQuery.delete} where [{deleteQuery.where}]")
        else:
            logging.error(f"Incorrect delete query. Multiple Delete is not supported. {deleteQuery.delete} where [{deleteQuery.where}]")
            raise Exception("Error occurred while running delete stmt")



    for updateQuery in queries.update:
        entry = []

        if updateQuery.where:
            entry = list(filter(lambda elem: len(elem.xpath(updateQuery.where)) > 0, xml_tree.xpath(f"{updateQuery.update}")))
        else:
            entry = xml_tree.xpath(f"{updateQuery.update}")

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
                print(f"insert into {targetElement}")
                print(f"attribute:{insertQuery.attribute['name']} value:{insertQuery.attribute['value']}")
                targetElement.set(insertQuery.attribute['name'], insertQuery.attribute['value'])
                print(f"value ({etree.tostring(targetElement)})")
        elif len(entry) == 0:
            logging.warning(f"Warning: Target Element not found {insertQuery.insert}")
        else:
            logging.error(f"Incorrect Insert query. You are trying to insert into multiple tags. Please check insert statement {etree.tostring(insertQuery.insert)}")
            raise Exception("Error: occurred while running insert stmt")

    return xml_prettify(xml_tree)
