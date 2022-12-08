from django.test import TestCase

tags = "aaaa,aaaa,aaaa,aaaa,aaaa"
if "," in tags:
    taglist = set(tags.replace(" ", "").split(","))
else:
    taglist = set(tags.replace(" ", ""))

print(taglist)
# replace 는 걍 둬도 되고 split , 하려고 하는데 , 가 없으면 문제
