import logging
import re

from utils.file_utils import *
from utils.yml_utils import *


# def replace_env_variable(_value):
#     env_var = re.fullmatch(r"\${(.+?)}", _value)
#     if env_var:
#         env_var = re.findall(r"{(.+?)}", env_var.string)[0]
#         for item, value in os.environ.items():
#             if item == env_var:
#                 return value
#         logging.warning("Environment variable [" + str(env_var) + "] not set.")
#     return _value


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
