from django.test import TestCase

tags = "aan,aa"
if "," in tags:
    taglist = set(tags.replace(" ", "").split(","))
else:
    taglist = tags.replace(" ", "")

print(taglist)
# replace 는 걍 둬도 되고 split , 하려고 하는데 , 가 없으면 문제
a = set(tags)
print(a)
