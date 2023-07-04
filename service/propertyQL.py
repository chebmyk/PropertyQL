import re
from model.messaging.messages import ConsoleLogObserver, logMsg
from model.query.properties.propertiesQuery import *
from service.messageService import MessageService


class PropertyQL:
    consoleLog = ConsoleLogObserver()
    messageService = MessageService()

    def __init__(self):
        self.messageService.subscribe(self.consoleLog)

    def run(self, properties, query: Query):

        assert properties is not None
        assert query is not None

        queries = Query(**query)
        result = properties
        result = self.run_delete_query(result, queries.delete)
        result = self.run_update_query(result, queries.update)
        result = self.run_insert_query(result, queries.insert)
        return result

    def run_delete_query(self, properties: str, deletes):
        result = []
        for line in properties:
            new_line = line
            match = re.search(property_regexp_pattern, line)
            if match:
                property = match.group().replace("=", "")
                property = property.strip()
                for deleteQuery in deletes:
                    if property == deleteQuery.delete:
                        self.messageService.publish(logMsg.info(f"Delete property: {property}"))
                        new_line = "#" + line
                        result.extend(["\n","# **Deleted value\n"])
            result.append(new_line)
        return result

    def run_update_query(self, properties: str, updates):
        result = []
        for line in properties:
            new_line = line
            match = re.search(property_regexp_pattern, line)
            if match:
                property = match.group().replace("=", "")
                property = property.strip()
                for updateQuery in updates:
                    if property == updateQuery.update:
                        self.messageService.publish(logMsg.info(f"Update property: {property}"))
                        self.messageService.publish(logMsg.info(f"Old value: {line}"))
                        new_line = updateQuery.update + "=" + updateQuery.value + "\n"
                        self.messageService.publish(logMsg.info(f"New value: {new_line}"))
                        result.extend(["\n","# **Updated value\n"])
            result.append(new_line)
        return result


    def run_insert_query(self, properties, inserts):
        if len(inserts)>0:
            property_set = self.get_property_set(properties)
            if len(inserts) > 0:
                properties.extend(["\n", "# ===== Start Block of generated Properties\n"])

            for insertQuery in inserts:
                if not insertQuery.insert in property_set:
                    self.messageService.publish(logMsg.info(f"Insert property: {insertQuery.insert}={insertQuery.value}"))
                    if insertQuery.comment:
                        properties.append("\n# " + insertQuery.comment + "\n")
                    properties.append(insertQuery.insert + "=" + insertQuery.value + "\n")
                else:
                    self.messageService.publish(logMsg.warning(f"Failed to insert: Property [{insertQuery.insert}] already exists."))

            if len(inserts) > 0:
                properties.extend(["\n", "# ===== End Block of generated Properties\n"])

        return properties


    def get_property_set(self, properties):
        property_set = set()
        for line in properties:
            match = re.search(r'^[^#]\s*(\w+(\.\w+)+|\w+)\s*=\s*', line)
            if match:
                property = match.group().replace("=", "").strip()
                property_set.add(property)

        return property_set