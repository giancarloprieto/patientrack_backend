def get_model_choices(data_class):
    return [(attr, getattr(data_class, attr)) for attr in dir(data_class) if
            isinstance(getattr(data_class, attr), str) and not attr.startswith('_')]
