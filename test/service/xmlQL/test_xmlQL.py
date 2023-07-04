import unittest

from mql.service import xmlQL  as xql
from mql.utils.file_utils import read_xml_file, read_yaml_file
from mql.utils.xml_utils import xml_prettify


class xmlQLTestCases(unittest.TestCase):


    def test_delete_tag(self):
        xml_tree = read_xml_file("cases/properties.xml")
        query = read_yaml_file("cases/delete/delete_element.ql")
        output = xql.XMLQl().run(xml_tree, query)
        expected = read_xml_file("cases/delete/delete_element_output.xml")
        self.assertEqual(output, xml_prettify(expected))

    def test_delete_attribute(self):
        xml_tree = read_xml_file("cases/properties.xml")
        query = read_yaml_file("cases/delete/delete_attribute.ql")
        output = xql.XMLQl().run(xml_tree, query)
        expected = read_xml_file("cases/delete/delete_attribute_output.xml")
        self.assertEqual(output, xml_prettify(expected))

    def test_update_tag(self):
        xml_tree = read_xml_file("cases/properties.xml")
        query = read_yaml_file("cases/update/update_tag_value.ql")
        output = xql.XMLQl().run(xml_tree, query)
        expected = read_xml_file("cases/update/update_tag_value_output.xml")
        self.assertEqual(output, xml_prettify(expected))

    def test_update_attribute(self):
        xml_tree = read_xml_file("cases/properties.xml")
        query = read_yaml_file("cases/update/update_attribute.ql")
        output = xql.XMLQl().run(xml_tree, query)
        expected = read_xml_file("cases/update/update_attribute_output.xml")
        self.assertEqual(output, xml_prettify(expected))


    def test_insert_tag(self):
        xml_tree = read_xml_file("cases/properties.xml")
        query = read_yaml_file("cases/insert/case_insert_element.ql")
        output = xql.XMLQl().run(xml_tree, query)
        expected = read_xml_file("cases/insert/case_insert_element_output.xml")
        self.assertEqual(output, xml_prettify(expected))

    def test_insert_attribute(self):
        xml_tree = read_xml_file("cases/properties.xml")
        query = read_yaml_file("cases/insert/case_insert_attribute.ql")
        output = xql.XMLQl().run(xml_tree, query)
        expected = read_xml_file("cases/insert/case_insert_attribute_output.xml")
        self.assertEqual(output, xml_prettify(expected))

    def test_insert_duplicate(self):
        xml_tree = read_xml_file("cases/properties.xml")
        query = read_yaml_file("cases/insert/negative/case_insert_duplicate_subelement.ql")
        with self.assertRaises(Exception):
            xql.XMLQl().run(xml_tree, query)

    def test_insert_tag_into_array(self):
        xml_tree = read_xml_file("cases/servers.xml")
        query = read_yaml_file("cases/insert/case_insert_element_into_array.ql")
        output = xql.XMLQl().run(xml_tree, query)
        expected = read_xml_file("cases/insert/case_insert_element_into_array_output.xml")
        self.assertEqual(output, xml_prettify(expected))


    def test_insert_duplicate_into_array(self):
        xml_tree = read_xml_file("cases/servers.xml")
        query = read_yaml_file("cases/insert/negative/case_insert_duplicate_element_into_array.ql")
        with self.assertRaises(Exception):
            xql.XMLQl().run(xml_tree, query)


if __name__ == '__main__':
    unittest.main()
