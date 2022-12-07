from django.test import TestCase

# a = {1, 2, 3, 4, 5, 6}
# c = set(range(7, 9))

# print(c.isdisjoint(a))

tag = "오늘, 아그냥, 호호 호호, 아이아 이"
if tag != "":
    tags = list(tag.replace(" ", "").split(","))
    for t in tags:
        print(t)
