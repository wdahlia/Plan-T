from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields["username"].label = "아이디"
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "아이디를 입력해주세요.",
                "class": "form-control mx-0",
                "style": "width: 100%; height: 50px;",
            }
        )

        self.fields["password1"].label = "비밀번호"
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "비밀번호를 입력해주세요.",
                "class": "form-control",
                "style": "width: 100%; height: 50px;",
            }
        )

        self.fields["password2"].label = "비밀번호 확인"
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "비밀번호를 한번 더 입력해주세요.",
                "class": "form-control",
                "style": "width: 100%; height: 50px;",
            }
        )

        self.fields["nickname"].label = "별명"
        self.fields["nickname"].widget.attrs.update(
            {
                "placeholder": "별명을 입력해주세요.",
                "class": "form-control",
                "style": "width: 100%; height: 50px;",
            }
        )       

        self.fields["email"].label = "이메일"
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": "예 : brokurly@brokurly.com",
                "class": "form-control mx-0",
                "style": "width: 100%; height: 50px;",
            }
        )       


    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2", "nickname", "email", ]