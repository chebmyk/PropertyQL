import os
import unittest

from deployment.scripts.utils.file_utils import read_file, read_yaml_file, write_file
from service.replaceToken import *


class ReplaceTokenTestCase(unittest.TestCase):

    def test_replace_token(self):
        output_file_name = "config_output.tmp"
        properties = read_yaml_file("test/case/service/replaceToken/property.yml")
        input_file = read_file("test/case/service/replaceToken/config_input.xml")

        os.environ["ENV_TYPE"] = "Dev"

        output_file = write_file(output_file_name)

        for line in input_file:
            line_new = replace_token(line, properties)
            output_file.write(line_new)
        output_file.close()

        result = read_file(output_file_name)
        expected = read_file("test/case/service/replaceToken/config_output.xml")

        self.assertEqual(result.read(), expected.read())

        result.close()
        expected.close()
        input_file.close()


    def test_replace_env_variables_in_text(self):
        ENV_TEST_VAR="/path/to/file"
        os.environ["ENV_TEST_VAR"] = ENV_TEST_VAR
        input = "Var is ${ENV_TEST_VAR}"
        result = replace_env_variable(input)
        self.assertEqual(result, "Var is "+ ENV_TEST_VAR)

    def test_replace_env_variables(self):
        ENV_TEST_VAR="/path/to/file"
        os.environ["ENV_TEST_VAR"] = ENV_TEST_VAR
        input = "${ENV_TEST_VAR}"
        result = replace_env_variable(input)
        self.assertEqual(result, ENV_TEST_VAR)

    def test_replace_env_two_variables(self):
        ENV_TEST_VAR="VAR"
        ENV_TEST_VAR2="VAR2"
        os.environ["ENV_TEST_VAR"] = ENV_TEST_VAR
        os.environ["ENV_TEST_VAR2"] = ENV_TEST_VAR2
        input = "${ENV_TEST_VAR}"+":"+"${ENV_TEST_VAR2}"
        result = replace_env_variable(input)
        self.assertEqual(result, ENV_TEST_VAR+":"+ENV_TEST_VAR2)


if __name__ == '__main__':
    unittest.main()