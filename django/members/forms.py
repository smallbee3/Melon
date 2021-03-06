from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

User = get_user_model()


__all__ = (
    'SignupForm',
)


class SignupForm(forms.Form):
    username = forms.CharField(
        label='아이디',
        # required=False

        # css를 주면 클래스를 지정해주어야함.
        # widget=forms.TexttInput(
        #     attrs={
        #         'class': ...
        #     }
        # )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError('이미 사용중인 아이디입니다.')
            # raise ValidationError를 하면 에러가 있을 경우 form.errors에 해당 내용을 넣어줌.
        return data
        # ex) 예를 들어서 쉼표로 데이터로 전달받을 수 있는  어떤 input 요소 폼을 가정.
        #     입력을 할 때 폼에 쉼표단위로 구분해서 넣으면 쉼표단위로 내가 좋아하는게
        #     태그로 정리 되야 할 때,
        #     ->
        #     validation을 거치는 동안 ','로 된 데이터를
        #     파이썬 리스트형 객체로 자동으로 변환해서 편하게 쓸 수 있음.
        #     (폼에서 가져온 데이터를 cleaned_data해서 그것을 꺼내서 리스트형태로 바꾸는 것이 아니라 그 과정 자체를 form안에다 추상화 시킬 수 있는 것)

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise ValidationError('비밀번호와 비밀번호 확인란의 값이 다릅니다.')
        return password
        # 리턴 안해주면 해당 필드에서 cleaned_data 꺼내올 때 에러가 발생함.


class LoginForm(forms.Form):
    username = forms.CharField(
        label='아이디',
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            print('가입되지 않은 사용자입니다.')
            raise ValidationError('가입되지 않은 사용자입니다.')
        return data

    def clean_password(self):
        # username = self.cleaned_data['username']
        username = self.cleaned_data.get('username')

        # 이 부분에서 가입되지 않은 아이디 경우에 계속 keyerror가 발생.
        # 고민한 결과 위의 validation에서 username에서 raise ValidationError가 발생하면
        # cleaned_data에 username이 들어가지 않아 이곳에서 Keyerror가 발생하는 것으로 판단함.
        # 값이 없어도 키를 호출할 수 있는 딕셔너리 호출 get()함수를 통해 문제 해결.

        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            print('비밀번호가 틀렸습니다.')
            raise ValidationError('비밀번호가 틀렸습니다.')
        return password
