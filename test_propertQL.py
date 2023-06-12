import unittest

from service.propertyQL import apply_config
from utils.file_utils import read_file, read_yaml_file, write_file


class xmlQLTestCases(unittest.TestCase):
    def test_update_property(self):
        prop_file = read_file("test/case/service/propertyQL/config.properties")
        query = read_yaml_file("test/case/service/propertyQL/update/case1.ql")
        output = write_file("output.tmp")
        output = apply_config(prop_file, query, output)
        output.close()
        expected = read_file("test/case/service/propertyQL/update/case1_output.properties")
        output = read_file("output.tmp")
        self.assertEqual(expected.read(), output.read())
        output.close()
        prop_file.close()
        expected.close()


    def test_insert_property(self):
        prop_file = read_file("test/case/service/propertyQL/config.properties")
        query = read_yaml_file("test/case/service/propertyQL/insert/case1.ql")
        output = write_file("output.tmp")
        output = apply_config(prop_file, query, output)
        output.close()
        expected = read_file("test/case/service/propertyQL/insert/case1_output.properties")
        output = read_file("output.tmp")
        self.assertEqual(expected.read(), output.read())
        output.close()
        prop_file.close()
        expected.close()


if __name__ == '__main__':
    unittest.main()
