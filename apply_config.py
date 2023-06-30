import pathlib
import shutil
import sys
import service.propertyQL
import service.xmlQL
from utils.file_utils import *


def validate_input_params(_params_):
    if len(_params_) < 2:
        print("Wrong input parameters")
        print("Expected parameters: {xml_file}, {query_file}")
        print(_params_)
        sys.exit(1)
    else:
        print("xml_file: " + _params_[1])
        print("query_file: " + _params_[2])


if __name__ == '__main__':

    validate_input_params(sys.argv)

    file_path= sys.argv[1]
    file_extension = pathlib.Path(file_path).suffix
    query_path = sys.argv[2]

    if file_extension in [".mxres",".xml"]:

        xml_tree = read_xml_file(file_path)
        query = read_yaml_file(query_path)

        xml_tree = service.XMLQl(xml_tree, query).apply_config()

        shutil.copy2(file_path, file_path + ".default")
        write_file(file_path).write(xml_tree)

    elif file_extension in [".properties",".sh",".props"]:

        output_file_path = "output.tmp"

        input_file = read_file(file_path)
        query = read_yaml_file(query_path)
        output_file = write_file(output_file_path)

        output_file = service.propertyQL.apply_config(input_file, query, output_file)
        output_file.close()

        shutil.copy2(file_path, file_path + ".default")
        shutil.copy2(output_file_path, file_path)
    else:
        raise Exception(f"Config files with extension [{file_extension}] are not supported")
