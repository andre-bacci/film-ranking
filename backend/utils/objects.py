def set_all_attrs(object, attributes: dict):
    for k, v in attributes.items():
        setattr(object, k, v)
    return object
