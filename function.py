def change_value(value):
    if value == "":
        index = value
        print("공백이 들어옴")
    else:
        hour, min = map(int, value.split(":"))
        index = ((hour - 6) * 6) + (min // 10)
        return int(index)


def create_tag(tags, Tag, todo):
    if tags != "":
        tags_ = tags.replace(" ", "")
        if "," in tags_:
            for tag in tags.split(",")[:5]:
                tag_ = tag.replace(" ", "")
                if tag_ != "":
                    Tag.objects.create(todo=todo, content=tag_)
        else:
            Tag.objects.create(todo=todo, content=tags_)
