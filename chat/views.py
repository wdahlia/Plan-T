from django.shortcuts import render
from random import randrange
from django.contrib.auth.decorators import login_required

anonymous_list = dict.fromkeys(range(1, 101), False)

# Create your views here.
@login_required
def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    if request.user.is_authenticated:
        nickname = request.user.username
    # 임시로 만들었다.
    # 비로그인 회원인 경우 1 ~ 100 까지의 값 중 중복이 안된 녀석을 끌고와서
    # 해당 고유값을 "anonymous user" 뒤에 붙인다.
    else:
        rnd = randrange(1, 101)
        while rnd in anonymous_list.keys():
            rnd = randrange(1, 101)

        anonymous_list[rnd] = True

        nickname = "anonymous user" + rnd

    context = {
        "room_name": room_name,
        "nickname": nickname,
    }

    return render(request, "chat/room.html", context)