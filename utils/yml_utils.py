import logging


def get_elem_value(_root, val_path):
    _result = str(get_elem(_root, val_path))
    return _result


def get_elem(_root, val_path):
    _result = None
    if val_path:
        _path = val_path.split(".")
        is_valid_path = True
        for el in _path:
            if el in _root:
                _root = _root[el]
            else:
                is_valid_path = False
                break
    if is_valid_path:
        _result = _root
    else:
        logging.warning('[' + val_path + '] element was not found!')
    return _result