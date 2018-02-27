from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    # /logout/
    # 문서에서 logout <- django logout 검색
    # GET요청이든 POST요청이든 상관없음
    logout(request)
    return redirect('index')

