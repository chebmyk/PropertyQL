import unittest
from mql.service import propertyQL as pql
from mql.utils.file_utils import read_file, read_yaml_file


class xmlQLTestCases(unittest.TestCase):
    def test_update_property(self):
        prop_file = read_file("cases/config.properties")
        query = read_yaml_file("cases/update/case1.ql")
        expected = read_file("cases/update/case1_output.properties")

        result = pql.PropertyQL().run(prop_file, query)
        self.assertEqual(expected.read(), "".join(result))

        prop_file.close()
        expected.close()


    def test_insert_property(self):
        prop_file = read_file("cases/config.properties")
        query = read_yaml_file("cases/insert/case1.ql")
        expected = read_file("cases/insert/case1_output.properties")

        result = pql.PropertyQL().run(prop_file, query)
        self.assertEqual(expected.read(), "".join(result))

        prop_file.close()
        expected.close()


if __name__ == '__main__':
    unittest.main()