from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
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


# 이름, 이메일, 주소 필드를 가져오려면
# 다중 상속을 할 수 밖에 없다.
class CustomUserChangeForm(PasswordChangeForm, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        
        self.fields["old_password"].label = ""
        self.fields["old_password"].widget.attrs.update(
            {
                "placeholder": "현재 비밀번호를 입력해주세요.",
                "class": "form-control",
                "style": "width: 100%; height: 50px;",
                "required": True,
            }
        )

        self.fields["new_password1"].label = ""
        self.fields["new_password1"].widget.attrs.update(
            {
                "placeholder": "새 비밀번호를 입력해주세요.",
                "class": "form-control",
                "style": "width: 100%; height: 50px;",
                "required": True,
            }
        )

        self.fields["new_password2"].label = ""
        self.fields["new_password2"].widget.attrs.update(
            {
                "placeholder": "새 비밀번호를 한번 더 입력해주세요.",
                "class": "form-control",
                "style": "width: 100%; height: 50px;",
                "required": True,
            }
        )

        self.fields["nickname"].label = ""
        self.fields["nickname"].widget.attrs.update(
            {
                "placeholder": "별명을 입력해주세요.",
                "class": "form-control",
                "style": "width: 100%; height: 50px;",
                "required": True,
            }
        )       

        self.fields["email"].label = ""
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": "예 : brokurly@brokurly.com",
                "class": "form-control mx-0",
                "style": "width: 100%; height: 50px;",
                "required": True,
            }
        )       
    
    
    # 데이터는 클라이언트로 부터 가져오지만
    # DB 에 저장하지 못한다. 
    # MRO : Method Resolution Order 때문인듯 하다.
    # link : https://engineer-mole.tistory.com/196
    def save(self):
        user = super().save(commit=True)

        # MRO 에 따라서 해결되지 않은 필드는 수작업으로 저장한다.
        user.nickname = self.cleaned_data["nickname"]
        user.email = self.cleaned_data["email"]

        user.save()

        return self.user


    class Meta:
        model = get_user_model()
        fields = ["old_password", "new_password1", "new_password2", "nickname", "email",]