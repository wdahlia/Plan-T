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


def check_time(request, today_todos, start, end, messages):
    exist = set()
    for todo in today_todos:
        if todo.started_at != "" and todo.expired_at != "":
            st = change_value(todo.started_at)
            ed = change_value(todo.expired_at)
            for t in range(st, ed + 1):
                exist.add(t)
    if (start != "") and (end != ""):
        timetable = set(range(change_value(start), change_value(end) + 1))
        if (start <= end) and (timetable.isdisjoint(exist)):
            return True
        else:
            messages.warning(request, "시간이 잘못되었습니다.")
            return False
    elif (start != "") and (end == ""):
        messages.error(request, "끝나는 시간을 입력해주세요.")
        return False
    elif (start == "") and (end != ""):
        messages.error(request, "시작 시간을 입력해주세요.")
        return False
