import unittest

from deployment.scripts.service.xmlQL import apply_config
from deployment.scripts.utils.file_utils import read_xml_file, read_yaml_file
from deployment.scripts.utils.xml_utils import xml_prettify


class xmlQLTestCases(unittest.TestCase):
    def test_update_tag(self):
        xml_tree = read_xml_file("test/case/service/xmlQL/properties.xml")
        query = read_yaml_file("test/case/service/xmlQL/update/case1.ql")
        output = apply_config(xml_tree, query)
        expected = read_xml_file("test/case/service/xmlQL/update/case1_output.xml")
        self.assertEqual(output, xml_prettify(expected))


    def test_insert_tag(self):
        xml_tree = read_xml_file("test/case/service/xmlQL/properties.xml")
        query = read_yaml_file("test/case/service/xmlQL/insert/case1.ql")
        output = apply_config(xml_tree, query)
        expected = read_xml_file("test/case/service/xmlQL/insert/case1_output.xml")
        self.assertEqual(output, xml_prettify(expected))

if __name__ == '__main__':
    unittest.main()
