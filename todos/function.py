def change_value(value):
    if value is None:
        index = value
        return index
    else:
        hour, min = map(int, value.split(":"))
        index = ((hour - 6) * 6) + (min // 10)
        return index
