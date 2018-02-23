from django.contrib.auth import authenticate, login, logout, get_user_model
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


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

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # 'auth.User' has been swapped for 'members.User' 오류떠서
        User = get_user_model()

        # if User.objects.filter(username__contains=username):
        #     # return HttpResponse('아이디겹침')
        #     return redirect('index')
        #
        # if password == password2:
        #     user = User.objects.create_superuser(username, '', password)
        #
        # return redirect('index')
        # exists()안쓰면?? 됬는데

        # if User.objects.filter(username==username).exists():
        #     # return HttpResponse('아이디겹침')
        #     print('Username already exists')
        #     # return redirect('index')
        # elif password == password2:
        #     print('Password and Password2 is not equal')
        # else:
        #     user = User.objects.create_superuser(username=username, password=password)
        #     return redirect('index')

        is_valid = True
        if User.objects.filter(username=username).exists():
            # return HttpResponse('아이디겹침')
            print('Username already exists')
            context['errors'].append('Username already exists')
            is_valid = False

        if password != password2:
            print('Password and Password2 is not equal')
            context['errors'].append('Password and Password2 is not equal')
            is_valid = False

        if is_valid:
            User.objects.create_superuser(username=username, password=password)
            return redirect('index')

    return render(request, 'members/signup.html', context)

