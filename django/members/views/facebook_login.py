import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate
from django.http import HttpResponse
from django.shortcuts import redirect

__all__ = (
    'facebook_login',
)


User = get_user_model()

# 1)
# 템플릿에서 a태그를 타고
# https://www.facebook.com/v2.12/dialog/oauth?client_id=100272904140135
# 로 갔다가
# redirect_uri=http://localhost:8000/facebook-login/
# 여기로 redirect해서 'code' 값을 받아옴

# 2)
# 위의 리다이렉트 된 주소를 config/urls.py에서 찾아보니 바로 이 뷰여서 여기로 옴.
# 그래서 클라이언트가 받아온 'code'값을 가지고
#


def facebook_login(request):
    # GET parameter가 왔을 것으로 가정
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    login(request, user)
    return redirect('index')


def facebook_login_backup(request):

    # url = 'https://graph.facebook.com/v2.12/oauth/access_token?client_id=100272904140135&redirect_uri=http://localhost:8000/facebook-login&client_secret=69546495d5613caafab5cb698ea9f9ce&code={code-parameter}'

    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CDDE
    code = request.GET['code']
    redirect_uri = 'http://localhost:8000/facebook-login/'

    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.get(url, params)
    # print(response)
    # print(response.text)

    response_dict = response.json()
    # for key, value in response_dict.items():
    #     print('')
    #     print(f'{key}: {value}')
    #     print('')

    # 지금 장고 로직에서 오랜만에 벗어났쬬.
    # return redirect('login')

    # return HttpResponse(response_dict['access_token'])

    url = 'https://graph.facebook.com/v2.12/me'
    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'picture.width(2500)',
            'first_name',
            'last_name',
        ])
    }
    response = requests.get(url, params)
    response_dict = response.json()

    # {'id': '1687143551366915', 'name': 'Youngki Song', 'picture': {'data': {'height': 1290, 'is_silhouette': True,
    #                                                                         'url': 'https://scontent.xx.fbcdn.net/v/t31.0-1/10506738_10150004552801856_220367501106153455_o.jpg?oh=83c91c0ef0bd53a4c7e77466b4b261ff&oe=5B1212BB',
    #                                                                         'width': 2048}}, 'first_name': 'Youngki',
    #  'last_name': 'Song'}

# 애플리케이션 별로 사용자에게 고유한 아이디
    # 아이디별이 아님.
    # 그냥 만들어도 보통은 중복이 안되요.

    facebook_id = response_dict['id']
    name = response_dict['name']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_picture = response_dict['picture']['data']['url']


    # get_or_create를 못씀, createuser해야되서

    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)
    else:


    # 원래 어센티케이티에서 검사했음.
    # 이제 유저를 인증하는 로직을 따로 만들어야함.
    # -> backends.py 만들고 장고문서보러 감.

        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
    login(request, user)
    return redirect('index')

    # return HttpResponse(str(response_dict))
