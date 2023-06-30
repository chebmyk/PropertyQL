import xml.dom.minidom

from lxml import etree


class XmlElement:

    def __init__(self, element):
        self.element = element
        self.childs = []

    def get_childs(self):
        return self.childs


def parse_xml(xml_string):
    return etree.fromstring(xml_string).getroottree()


def xml_look_up(xml_object, xpath, elem):
    if xpath != '':
        if elem is not None and not xpath.startswith("/"):
            elem_val = elem.xpath(xpath)
            if elem_val is not None and len(elem_val) > 0:
                if len(elem_val) == 1:
                    return elem_val[0]
                else:
                    return elem_val
        else:
            xpath_value = xml_object.xpath(f"{xpath}")
            if xpath_value is not None and len(xpath_value) > 0:
                if len(xpath_value) == 1:
                    return xpath_value[0]
                else:
                    return xpath_value
    return ''


def element_to_xpath_list(_element_):
    xpath_list = []

    if not type(_element_) is etree._Comment:

        element_string = etree.tostring(_element_, encoding='utf-8', pretty_print=True)
        root = parse_xml(element_string)

        sub_elements = root.xpath('//*')
        xpath_list = []

        for elem in sub_elements:

            xpath = root.getpath(elem)
            value = elem.text.strip() if elem.text else ""

            # Collect element tags with values =============
            if value:
                val = {'xpath': xpath, 'value': value}
                xpath_list.append(val)

            # Collect element attributes ===================
            for attrib in elem.attrib:
                xpath = root.getpath(elem) + "/@" + attrib
                value = elem.get(attrib)
                val = {'xpath': xpath, 'value': value}
                xpath_list.append(val)

    return xpath_list


def check_duplicates(root, element):
    new_element = element_to_xpath_list(element)
    root =  etree.fromstring(etree.tostring(root))
    sub_elements = root.getchildren()

    has_duplicate = False
    for child in sub_elements:
        if not type(child) is etree._Comment:
            current = element_to_xpath_list(child)

            if len(new_element) == len(current):
                for tag in current:
                    # print(f"{tag['xpath']}: {tag['value']}")
                    if list(filter(lambda el: el['xpath'] == tag['xpath'].replace("/"+root.tag,"") and el['value'] == tag['value'], new_element)):
                        has_duplicate = True
                    else:
                        has_duplicate = False
                        break

            if has_duplicate:
                break
    return has_duplicate


def xml_prettify(_xml_tree_):
    #xml =  xml.dom.minidom.parseString(etree.tostring(_xml_tree_))  # or xml.dom.minidom.parseString(xml_string)
    xml_root = xml.dom.minidom.parseString(etree.tostring(_xml_tree_))
    return '\n'.join([line for line in xml_root.toprettyxml(indent=' '*2).split('\n') if line.strip()])