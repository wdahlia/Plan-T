from django.shortcuts import redirect
from django.contrib import messages

# login decorator
# GET, POST method 가 다 쓰이는 method 에 적용
# link : https://parkhyeonchae.github.io/2020/03/25/django-project-05/
# 로그인 확인
def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "로그인한 사용자만 이용할 수 있습니다.")
            
            return redirect("accounts:login")
        
        return function(request, *args, **kwargs)
    
    return wrap