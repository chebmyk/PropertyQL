import unittest

from service.xmlQL import apply_config
from utils.file_utils import read_xml_file, read_yaml_file
from utils.xml_utils import xml_prettify


class xmlQLTestCases(unittest.TestCase):
    def test_update_tag(self):
        xml_tree = read_xml_file("test/case/service/xmlQL/properties.xml")
        query = read_yaml_file("test/case/service/xmlQL/update/update_tag_value.ql")
        output = apply_config(xml_tree, query)
        expected = read_xml_file("test/case/service/xmlQL/update/update_tag_value_output.xml")
        self.assertEqual(output, xml_prettify(expected))

    def test_update_attribute(self):
        xml_tree = read_xml_file("test/case/service/xmlQL/properties.xml")
        query = read_yaml_file("test/case/service/xmlQL/update/update_attribute.ql")
        output = apply_config(xml_tree, query)
        expected = read_xml_file("test/case/service/xmlQL/update/update_attribute_output.xml")
        self.assertEqual(output, xml_prettify(expected))


    def test_insert_tag(self):
        xml_tree = read_xml_file("test/case/service/xmlQL/properties.xml")
        query = read_yaml_file("test/case/service/xmlQL/insert/case_insert_element.ql")
        output = apply_config(xml_tree, query)
        expected = read_xml_file("test/case/service/xmlQL/insert/case_insert_element_output.xml")
        self.assertEqual(output, xml_prettify(expected))

    def test_insert_attribute(self):
        xml_tree = read_xml_file("test/case/service/xmlQL/properties.xml")
        query = read_yaml_file("test/case/service/xmlQL/insert/case_insert_attribute.ql")
        output = apply_config(xml_tree, query)
        expected = read_xml_file("test/case/service/xmlQL/insert/case_insert_attribute_output.xml")
        self.assertEqual(output, xml_prettify(expected))


if __name__ == '__main__':
    unittest.main()
