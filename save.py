import shelve


def get_data(var_name: str, filename: str):
    with shelve.open(filename) as save:
        data = save[var_name]
    return data


def save_data(var_name: str, value: object, filename: str):
    with shelve.open(filename) as save:
        save[var_name] = value
