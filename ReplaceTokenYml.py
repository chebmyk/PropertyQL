import sys
from mql.utils.file_utils import *


def validate_input_params(_params_):
    if len(_params_) < 2:
        print("Wrong input parameters")
        print("Expected parameters: {input_file_path}, {property_file_path}")
        print("{input_file_path} - input xml file with placeholder")
        print("{property_file_path} - path to the property file which contains property values")
        print(_params_)
        sys.exit(1)
    else:
        print("Input file path: " + _params_[1])
        print("Property file path: " + _params_[2])


if __name__ == '__main__':

    validate_input_params(sys.argv)

    input_file = sys.argv[1]
    property_file = sys.argv[2]
    properties = read_yaml_file(property_file)

    if len(sys.argv) > 3:
        output_file_name = sys.argv[3]
    else:
        output_file_name = "output_file.xml"

    properties = read_yaml_file(property_file)
    file = read_file(input_file)
    output_file = write_file(output_file_name)

    counter = 1
    for line in file:
        line_new = replace_token(line, properties)
        counter += 1
        output_file.write(line_new)

    output_file.close()
    file.close()

