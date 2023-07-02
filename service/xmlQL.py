import logging
from xml.etree.ElementTree import ElementTree
from model.messaging.messages import LogMessage, ConsoleLogObserver
from model.query.xml.xmlQuery import Query
from service.messageService import *
from utils.file_utils import *
from utils.xml_utils import *


class XMLQl:
    xml_tree: ElementTree
    query: Query
    consoleLog = ConsoleLogObserver()
    messageService = MessageService()
    log = LogMessage()
    

    def __init__(self, xml_tree, query):
        assert xml_tree is not None
        assert query is not None
        self.messageService.subscribe(self.consoleLog)
        self.xml_tree = xml_tree
        self.query = query

    def run(self):
        queries = Query(**self.query)
        self.run_delete_query(queries.delete)
        self.run_update_query(queries.update)
        self.run_insert_query(queries.insert)
        return xml_prettify(self.xml_tree)

    def run_delete_query(self, deletes):
        for deleteQuery in deletes:
            entry = []
            if deleteQuery.where:
                entry = list(filter(lambda elem: len(elem.xpath(deleteQuery.where)) > 0,
                                    self.xml_tree.xpath(f"{deleteQuery.delete}")))
            else:
                entry = self.xml_tree.xpath(f"{deleteQuery.delete}")

            if len(entry) == 1:
                self.messageService.publish_event(self.log.logInfo(f"Delete from Object: {etree.tostring(entry[0])}"))
                found = entry[0].xpath(deleteQuery.element)
                if found:
                    element = found[0]
                    if isinstance(element, elTree._Element):
                        self.messageService.publish_event(self.log.logInfo(f"Element: {element.tag}"))
                        element.getparent().remove(element)
                    else:
                        start = deleteQuery.element.rindex("@")
                        attribute_name = deleteQuery.element[start + 1:]
                        self.messageService.publish_event(self.log.logInfo(f"Attribute: {attribute_name}"))
                        element.getparent().attrib.pop(attribute_name, None)
                else:
                    self.messageService.publish_event(self.log.logWarn(f"Updated field [{deleteQuery.element}] doesn't exists"))

            elif len(entry) == 0:
                self.messageService.publish_event(self.log.logWarn("No Records found to delete"))
                self.messageService.publish_event(self.log.logWarn(f"{deleteQuery.delete} where [{deleteQuery.where}]"))
            else:
                self.messageService.publish_event(self.log.logError(
                    f"Incorrect delete query. Multiple Delete is not supported. {deleteQuery.delete} where [{deleteQuery.where}]"))
                raise Exception("Error occurred while running delete stmt")

    def run_update_query(self, updates):
        for updateQuery in updates:
            entry = []

            if updateQuery.where:
                entry = list(filter(lambda elem: len(elem.xpath(updateQuery.where)) > 0,
                                    self.xml_tree.xpath(f"{updateQuery.update}")))
            else:
                entry = self.xml_tree.xpath(f"{updateQuery.update}")

            if len(entry) == 1:
                self.messageService.publish_event(self.log.logInfo(f"Update Object: {etree.tostring(entry[0])}"))

                element = entry[0].xpath(updateQuery.element)
                if element:
                    element = element[0]
                    if isinstance(element, elTree._Element):
                        self.messageService.publish_event(self.log.logInfo(f"Old value: {etree.tostring(element)}"))
                        element.text = updateQuery.value
                        self.messageService.publish_event(self.log.logInfo(f"New value: {etree.tostring(element)}"))
                    else:
                        self.messageService.publish_event(self.log.logInfo(f"Old value: {etree.tostring(element.getparent())}"))
                        element.getparent().set(element.attrname, updateQuery.value)
                        self.messageService.publish_event(self.log.logInfo(f"New value: {etree.tostring(element.getparent())}"))
                else:
                    self.messageService.publish_event(self.log.logWarn(f"Updated field [{updateQuery.element}] doesn't exists"))

            elif len(entry) == 0:
                self.messageService.publish_event(self.log.logWarn("No Records found for update"))
                self.messageService.publish_event(self.log.logWarn(f"{updateQuery.update}[{updateQuery.where}]"))
            else:
                self.messageService.publish_event(self.log.logError(
                    f"Incorrect update query. Multiple update is not supported. {etree.tostring(updateQuery.update)}[{etree.tostring(updateQuery.where)}]"))
                raise Exception("Error occurred while running update stmt")

    def run_insert_query(self, inserts):
        for insertQuery in inserts:
            entry = self.xml_tree.xpath(f"{insertQuery.insert}")
            if len(entry) == 1:
                targetElement = entry[0]
                if insertQuery.element:
                    self.messageService.publish_event(self.log.logInfo(f"insert into {self.xml_tree.getpath(targetElement)}"))
                    newElement = etree.fromstring(insertQuery.element)

                    if check_duplicates(targetElement, newElement):
                        self.messageService.publish_event(self.log.logError(f"Item already exists. {etree.tostring(newElement)} "))
                        raise Exception(f"Error: Item already exists. {etree.tostring(newElement)} ")

                    targetElement.append(newElement)
                    self.messageService.publish_event(self.log.logInfo(f"value ({etree.tostring(newElement)})"))
                elif insertQuery.attribute:
                    self.messageService.publish_event(self.log.logInfo(f"insert into {targetElement}"))
                    self.messageService.publish_event(self.log.logInfo(f"attribute:{insertQuery.attribute['name']} value:{insertQuery.attribute['value']}"))
                    targetElement.set(insertQuery.attribute['name'], insertQuery.attribute['value'])
                    self.messageService.publish_event(self.log.logInfo(f"value ({etree.tostring(targetElement)})"))
            elif len(entry) == 0:
                self.messageService.publish_event(self.log.logWarn(f"Target Element not found {insertQuery.insert}"))
            else:
                self.messageService.publish_event(self.log.logError(
                    f"Incorrect Insert query. You are trying to insert into multiple tags. Please check insert statement {etree.tostring(insertQuery.insert)}"))
                raise Exception("Error: occurred while running insert stmt")
