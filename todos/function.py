def change_value(value):
    if value is None:
        index = value
        return index
    # 데이터를 None에서 => ""로 바뀌었음. 이건 임시
    elif value == "":
        index = value
        print("공백이 들어옴")
    #
    else:
        hour, min = map(int, value.split(":"))
        index = ((hour - 6) * 6) + (min // 10)
        return int(index)
