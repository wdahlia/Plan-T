def change_value(value):
    if value == "":
        index = value
        print("공백이 들어옴")

    else:
        hour, min = map(int, value.split(":"))
        index = ((hour - 6) * 6) + (min // 10)
        return int(index)
