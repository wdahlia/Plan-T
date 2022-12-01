from django.test import TestCase

a = {1, 2, 3, 4, 5, 6}
c = set(range(5, 9))
if c.isdisjoint(a):
    print("참")
else:
    print("거짓")

print(c)
