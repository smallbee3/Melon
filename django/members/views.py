from django.contrib.auth import authenticate, login, logout, get_user_model
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.forms import SignupForm

User = get_user_model()


def login_view(request):
    # POST요청일때는
    # authentictate -> login후 'index'로 redirect
    #   실패시에는 다시 GET요청의 로직으로 이동
    #
    # GET요청일때는
    # members/login.html파일을 보여줌
    #   해당 파일의 form에는 username, password input과 '로그인'버튼이 있음
    #   form은 method POST로 다시 이 view로의 action(빈 값)을 가짐
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'members/login.html')


def logout_view(request):

    logout(request)
    return redirect('index')


def signup_view(request):
    # /signup/
    # username,password, password2가 전달되었다는 가정
    # username이 중복되는지 검사, 존재하지 않으면 유저 생성 후 index로 이동
    # 이외의 경우는 다시 회원가입화면으로
    context = {
        'errors': [],
    }

    signup_form = SignupForm()

    # SignupForm 인스턴스를 생성
    # 생성한 인스턴스를 context에 전달
    # 전달받은 변수를 템플릿에서 변수 렌더링
    # 어떻게 나오나 보기
    context['signup_form'] = signup_form

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            is_valid = True
            if User.objects.filter(username=username).exists():
                form.add_error('username', '이미 사용되고 있는 아이디입니다.')
                is_valid = False

            if password != password2:
                form.add_error('password2', '비밀번호와 비밀번호 확인란의 값이 다릅니다.')
                is_valid = False

            if is_valid:
                # create_superuser의 경우에는 email이 필수?
                User.objects.create_user(username=username, password=password)
                return redirect('index')

    else:
        form = SignupForm()
    context = {
        'signup_form': form,
        # (만약에 validation을 거치지 못한) get요청의 경우에는
    }

        # username = request.POST['username']
        # password = request.POST['password']
        # password2 = request.POST['password2']
        #
        # # 'auth.User' has been swapped for 'members.User' 오류떠서
        # User = get_user_model()
        #
        # # 1) 수업시간 실습 - 나
        # # if User.objects.filter(username__contains=username):
        # #     # return HttpResponse('아이디겹침')
        # #     return redirect('index')
        # #
        # # if password == password2:
        # #     user = User.objects.create_superuser(username, '', password)
        # #
        # # return redirect('index')
        # # exists()안쓰면?? 됬는데
        #
        #
        # # 2) 수업시간 실습
        # # if User.objects.filter(username==username).exists():
        # #     # return HttpResponse('아이디겹침')
        # #     print('Username already exists')
        # #     # return redirect('index')
        # # elif password == password2:
        # #     print('Password and Password2 is not equal')
        # # else:
        # #     user = User.objects.create_superuser(username=username, password=password)
        # #     return redirect('index')
        #
        # is_valid = True
        # if User.objects.filter(username=username).exists():
        #     # return HttpResponse('아이디겹침')
        #     print('Username already exists')
        #     context['errors'].append('Username already exists')
        #     is_valid = False
        #
        # if password != password2:
        #     print('Password and Password2 is not equal')
        #     context['errors'].append('Password and Password2 is not equal')
        #     is_valid = False
        #
        # if is_valid:
        #     # create_superuser의 경우에는 email이 필수?
        #     User.objects.create_user(email='', username=username, password=password)
        #     return redirect('index')

    return render(request, 'members/signup.html', context)

