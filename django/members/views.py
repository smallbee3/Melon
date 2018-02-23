from django.contrib.auth import authenticate, login
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
