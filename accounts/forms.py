from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    UserChangeForm,
)
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password1",
            "password2",
            "nickname",
            "email",
        ]


# 이름, 이메일, 주소 필드를 가져오려면
# 다중 상속을 할 수 밖에 없다.
class CustomUserChangeForm(PasswordChangeForm, UserChangeForm):

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
        fields = [
            "old_password",
            "new_password1",
            "new_password2",
            "nickname",
            "email",
        ]
