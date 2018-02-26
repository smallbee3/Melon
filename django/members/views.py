from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.forms import SignupForm, LoginForm

# User class를 불러올 때는 get_user_model이라는 내장함수를 사용.
User = get_user_model()

# User 불러올 때 주의할 것!
# 아래 둘다 아님.
# from django.contrib.auth.models import User (x)  -> 안됨
#                                             auth.models을 쓰고 있지 않으니까.
#                                             auth.model로 우리가 정의한
#                                             커스텀유저모델을 쓰고 있음.
# from members.models import User (x) -> 되긴 되는데 별로 권장하는 방법이아님.





def login_view(request):
    # POST요청일때는
    # authentictate -> login후 'index'로 redirect
    #   실패시에는 다시 GET요청의 로직으로 이동
    #
    # GET요청일때는
    # members/login.html파일을 보여줌
    #   해당 파일의 form에는 username, password input과 '로그인'버튼이 있음
    #   form은 method POST로 다시 이 view로의 action(빈 값)을 가짐
    # if request.method == 'POST':
    #
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('index')
    # return render(request, 'members/login.html')

    # 2/24 로그인 뷰 form으로 구현해보기
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')

    else:
        form = LoginForm()
    context = {
        'login_form': form,
    }
    return render(request, 'members/login.html', context)




def logout_view(request):
    # /logout/
    # 문서에서 logout <- django logout 검색
    # GET요청이든 POST요청이든 상관없음
    logout(request)
    return redirect('index')



# def signup_view(request):
#
#     # /signup/
#     # username,password, password2가 전달되었다는 가정
#     # username이 중복되는지 검사, 존재하지 않으면 유저 생성 후 index로 이동
#     # 이외의 경우는 다시 회원가입화면으로
#     context = {
#             'errors': [],
#         }
#
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#
#         # 'auth.User' has been swapped for 'members.User' 오류떠서
#         User = get_user_model()
#
#
#         # 1) 수업시간 실습
#         # if User.objects.filter(username=username).exists():
#         #     print('Username already exists')
#         #
#         # elif password != password2:
#         #     print('Password and Password2 is not equal')
#         #
#         # else:
#         #     User.objects.create_superuser(username=username, password=password)
#         #     return redirect('index')
#
#
#         # 2) 아이디와 비밀번호 validation을 모두 하고 싶을 때 구조
#         is_valid = True
#         if User.objects.filter(username=username).exists():
#             context['errors'].append('Username already exists')
#             is_valid = False
#
#         if password != password2:
#             context['errors'].append('Password and Password2 is not equal')
#             is_valid = False
#
#         if is_valid:
#             # create_superuser의 경우에는 email이 필수?
#             User.objects.create_user(email='', username=username, password=password)
#             return redirect('index')
#
#     return render(request, 'members/signup.html', context)



# 3)    2/23 폼 관련 첫 실습 - Signup 폼으로 만들어보기

#       1) 실습 a
#       SignupForm 인스턴스를 생성
#       생성한 인스턴스를 context에 전달
#       전달받은 변수를 템플릿에서 변수 렌더링
#       어떻게 나오나 보기
#       -> 이 내용은 삭제함.

#       2) 실습 b
#       validation 코드 넣기
#       -> 바로 아래 코드


#       3) 실습 c
#       forms.py에서 에러메시지 설정하도록 변경
#       위 4)의 방법은 에러 출력자체는 편해졌지만
#       여전히 검증 로직이 너무나 불편.
#       -> views.py에서 is_valid()가 호출하는 동안
#          forms.py의 clean_<fieldname>()이 호출이 되면서
#          그곳에서 validation 검증을 하는 과정에서 에러가 발생한 것.


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # 유효성 검사를 하기 위해서
        # 데이터가 바인딩된(request.POST를 넣음) bound form을 생성
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 방법 1 - view.py에서 validation, 이런 로직을 직접구현해야해서 불편함
            # password2 = form.cleaned_data['password2']
            # is_valid = True
            # if User.objects.filter(username=username).exists():
            #     form.add_error('username', '이미 사용중인 아이디입니다.')
            #     is_valid = False
            # if password != password2:
            #     form.add_error('password2', '비밀번호와 비밀번호 확인란의 값이 다릅니다.')
            #     is_valid = False
            #
            # if is_valid:
            #     User.objects.create_user(username=username, password=password)
            #     return redirect('index')

            # 방법 2 - form.py에서 validation 작업.
            User.objects.create_user(username=username, password=password)
            # return redirect('index')

            # 회원가입 후 바로 로그인하는 비지니스 로직 추가
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return redirect('index')

    else:
        form = SignupForm()
        # GET요청의 경우에는 빈폼을 생성해서 context에 넣어줌.
        # 반대로 validation을 거치지 못한 POST요청의 경우 위에서 넣어준
        #       SignupForm(request.POST)가 계속 유효하기 때문에
        #       입력한 데이터가 아래 context에 전달되서 signup 화면에 다시 렌더링됨.

    # parent_tempalte = get_template('base.html')
    # print(type(parent_tempalte))

    context = {
        'signup_form': form,

        # 동적으로 템플릿을 전달할 때
        # 'parent': 'base.html',
        # 'parent': parent_tempalte,
    }
    return render(request, 'members/signup.html', context)

