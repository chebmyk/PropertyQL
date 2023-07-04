import os

import lxml.etree as elTree
import pandas as pd
import yaml
from jproperties import Properties


def read_xml_file(filename):
    return elTree.parse(filename)


def read_xml_root(filename):
    tree = read_xml_file(filename)
    item = tree.getroot()
    return item


def read_csv_file(filename):
    csv_data = pd.read_csv(filename,
                           sep=';',
                           encoding='utf-8',
                           header='infer',
                           index_col=False,
                           na_filter=False,
                           dtype=str)
    return csv_data


def read_properties_file(filename):
    configs = Properties()
    with open(filename, 'rb') as properties:
        configs.load(properties)
    return configs


def read_json_file(filename):
    with open(filename) as file:
        return yaml.safe_load(file) or {}


def read_yaml_file(filename):
    with open(filename) as file:
        return yaml.safe_load(file) or {}


def read_file(filename):
    return open(filename, errors='replace')


def write_file(filename):
    return open(filename, "w")


def file_extension(filename):
    return os.path.splitext(filename)[1]


def file_exists(filename):
    return os.path.exists(filename)


