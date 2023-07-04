import re

from mql.utils.file_utils import *
from mql.utils.yml_utils import *



def replace_env_variable(_value):
    placeholders = re.findall(r"\${(.+?)}", _value)
    line_new = _value

    for placeholder in placeholders:
        found = False
        for env_var, value in os.environ.items():
            if env_var == placeholder:
                line_new = line_new.replace("${"+placeholder+"}", value)
                found = True

        if not found:
            logging.warning("Environment variable [" + str(env_var) + "] not set.")

    return line_new


def replace_token(input_str, properties):
    placeholders = re.findall(r"\${(.+?)}", input_str)
    line_new = input_str

    for property_name in placeholders:
        value = get_elem_value(properties, property_name)
        value = replace_env_variable(value)
        placeholder = "${"+property_name+"}"
        line_new = line_new.replace(placeholder, value)

    return line_new
