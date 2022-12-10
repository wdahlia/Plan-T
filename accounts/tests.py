from django.test import TestCase
import operator

# Create your tests here.

tag = "asdf,f,,,,dsdf"
a = tag.split(",")
for b in a:
    if b == "":
        print(b)
# tag_count = {}

# for t in tag:
#     if t in tag_count:
#         tag_count[t] += 1
#     else:
#         tag_count[t] = 1

# sorted_count = sorted(tag_count.items(), key=operator.itemgetter(1), reverse=True)

# print(tag_count)
# print(sorted_count)
