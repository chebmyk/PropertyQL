import re
import sys
from mql.utils.file_utils import *

#from jproperties import Properties


if __name__ == '__main__':

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print("Input File: " + input_file)

        if sys.argv[2]:
            property_file = sys.argv[2]
            config = read_properties_file(property_file)
    else:
        print("Wrong input parameters")
        print("Expected parameters: {input_file_path}, {property_file_path}")
        print("{input_file_path} - input xml file")
        print("{property_file_path} -  file which contains property values")
        print(sys.argv)
        sys.exit(1)

    file = read_file(input_file)
    output_file = write_file("output_file.xml")

    counter = 1

    for line in file:
        placeholders = re.findall(r"{(.+?)}", line)
        # print(f"Parsing line {counter}")
        # print(f"Placeholders {placeholders}")
        line_new = line

        for prop in placeholders:
            value = config.get(prop).data
            placeholder = "${"+prop+"}"
            line_new = line_new.replace(placeholder, value)

        counter += 1
        output_file.write(line_new)


    # todo ADD evironment variables replacement
    # for item, value in os.environ.items():
    #     print('{}={}'.format(item, value))
    output_file.close()
    file.close()

