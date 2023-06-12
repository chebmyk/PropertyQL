import re

def replace_idx(_string_):
    return re.sub(r'\[\d+\]', '', _string_)
