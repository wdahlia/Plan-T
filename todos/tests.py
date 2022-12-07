from django.test import TestCase

# a = {1, 2, 3, 4, 5, 6}
# c = set(range(7, 9))

# print(c.isdisjoint(a))

# true = c와 a 가 겹치는 게 없다
from datetime import datetime, timedelta

few_week = 0  # int(few_week)
next_ = +1
last_ = -1
today = datetime.today().weekday() + 1
now = datetime.now()
week = now + timedelta(weeks=few_week, days=-(today % 7))
print("today :", today)
print("현재 : ", now)
print("기준 날짜 : ", week)
