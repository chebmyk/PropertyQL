from mql.model.messaging.messages import ConsoleLogObserver, logMsg
from mql.model.query.xml.xmlQuery import Query
from mql.service.messageService import MessageService
from mql.utils.file_utils import *
from mql.utils.xml_utils import *


class XMLQl:
    consoleLog = ConsoleLogObserver()
    messageService = MessageService()

    def __init__(self):
        self.messageService.subscribe(self.consoleLog)

    def run(self, xml_tree, query):

        assert xml_tree is not None
        assert query is not None

        queries = Query(**query)
        self.run_delete_query(xml_tree, queries.delete)
        self.run_update_query(xml_tree, queries.update)
        self.run_insert_query(xml_tree, queries.insert)
        return xml_prettify(xml_tree)

    def run_delete_query(self, xml_tree, deletes):
        for deleteQuery in deletes:
            entry = []
            if deleteQuery.where:
                entry = list(filter(lambda elem: len(elem.xpath(deleteQuery.where)) > 0,
                                    xml_tree.xpath(f"{deleteQuery.delete}")))
            else:
                entry = xml_tree.xpath(f"{deleteQuery.delete}")

            if len(entry) == 1:
                self.messageService.publish(logMsg.info(f"Delete from Object: {etree.tostring(entry[0])}"))
                found = entry[0].xpath(deleteQuery.element)
                if found:
                    element = found[0]
                    if isinstance(element, elTree._Element):
                        self.messageService.publish(logMsg.info(f"Element: {element.tag}"))
                        element.getparent().remove(element)
                    else:
                        start = deleteQuery.element.rindex("@")
                        attribute_name = deleteQuery.element[start + 1:]
                        self.messageService.publish(logMsg.info(f"Attribute: {attribute_name}"))
                        element.getparent().attrib.pop(attribute_name, None)
                else:
                    self.messageService.publish(logMsg.warning(f"Updated field [{deleteQuery.element}] doesn't exists"))

            elif len(entry) == 0:
                self.messageService.publish(logMsg.warning("No Records found to delete"))
                self.messageService.publish(logMsg.warning(f"{deleteQuery.delete} where [{deleteQuery.where}]"))
            else:
                self.messageService.publish(logMsg.error(f"Incorrect delete query. Multiple Delete is not supported. {deleteQuery.delete} where [{deleteQuery.where}]"))
                raise Exception("Error occurred while running delete stmt")

    def run_update_query(self, xml_tree, updates):
        for updateQuery in updates:
            entry = []

            if updateQuery.where:
                entry = list(filter(lambda elem: len(elem.xpath(updateQuery.where)) > 0,
                                    xml_tree.xpath(f"{updateQuery.update}")))
            else:
                entry = xml_tree.xpath(f"{updateQuery.update}")

            if len(entry) == 1:
                self.messageService.publish(logMsg.info(f"Update Object: {etree.tostring(entry[0])}"))
                element = entry[0].xpath(updateQuery.element)
                if element:
                    element = element[0]
                    if isinstance(element, elTree._Element):
                        self.messageService.publish(logMsg.info(f"Old value: {etree.tostring(element)}"))
                        element.text = updateQuery.value
                        self.messageService.publish(logMsg.info(f"New value: {etree.tostring(element)}"))
                    else:
                        self.messageService.publish(logMsg.info(f"Old value: {etree.tostring(element.getparent())}"))
                        element.getparent().set(element.attrname, updateQuery.value)
                        self.messageService.publish(logMsg.info(f"New value: {etree.tostring(element.getparent())}"))
                else:
                    self.messageService.publish(logMsg.warning(f"Updated field [{updateQuery.element}] doesn't exists"))

            elif len(entry) == 0:
                self.messageService.publish(logMsg.warning("No Records found for update"))
                self.messageService.publish(logMsg.warning(f"{updateQuery.update}[{updateQuery.where}]"))
            else:
                self.messageService.publish(logMsg.error(f"Incorrect update query. Multiple update is not supported. {etree.tostring(updateQuery.update)}[{etree.tostring(updateQuery.where)}]"))
                raise Exception("Error occurred while running update stmt")

    def run_insert_query(self, xml_tree, inserts):
        for insertQuery in inserts:
            entry = xml_tree.xpath(f"{insertQuery.insert}")
            if len(entry) == 1:
                targetElement = entry[0]
                if insertQuery.element:
                    self.messageService.publish(logMsg.info(f"insert into {insertQuery.insert}"))
                    newElement = etree.fromstring(insertQuery.element)

                    if check_duplicates(targetElement, newElement):
                        self.messageService.publish(logMsg.error(f"Item already exists. {etree.tostring(newElement)} "))
                        raise Exception(f"Error: Item already exists. {etree.tostring(newElement)} ")

                    targetElement.append(newElement)
                    self.messageService.publish(logMsg.info(f"value ({etree.tostring(newElement)})"))
                elif insertQuery.attribute:
                    self.messageService.publish(logMsg.info(f"insert into {targetElement}"))
                    self.messageService.publish(logMsg.info(f"attribute:{insertQuery.attribute['name']} value:{insertQuery.attribute['value']}"))
                    targetElement.set(insertQuery.attribute['name'], insertQuery.attribute['value'])
                    self.messageService.publish(logMsg.info(f"value ({etree.tostring(targetElement)})"))
            elif len(entry) == 0:
                self.messageService.publish(logMsg.warning(f"Target Element not found {insertQuery.insert}"))
            else:
                self.messageService.publish(logMsg.error(f"Incorrect Insert query. You are trying to insert into multiple tags. Please check insert statement {etree.tostring(insertQuery.insert)}"))
                raise Exception("Error: occurred while running insert stmt")