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
# 그래서 클라이언트가 받아온 'code'값을 가지고 이 뷰로 옴

# 3)
# 사용자가 가져온 이 값을 장고에서 토스 받아서


def facebook_login(request):
    # GET parameter가 왔을 것으로 가정
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    login(request, user)
    return redirect('index')


def facebook_login_backup(request):

    # url = 'https://graph.facebook.com/v2.12/oauth/access_token?client_id=100272904140135&redirect_uri=http://localhost:8000/facebook-login&client_secret=69546495d5613caafab5cb698ea9f9ce&code={code-parameter}'

    # code로부터 AccessToken 가져오기
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CODE
    # 페이스북로그인 버튼을 누른 후, 사용자가 승인하면 redirect_uri에 GET parameter로 'code'가 전송됨
    # 이 값과 client_id, secret을 사용해서 Facebook서버에서 access_token을 받아와야 함
    code = request.GET['code']
    # 이전에 페이스북 로그인 버튼을 눌렀을 때 'code'를 다시 전달받은 redirect_uri값을 그대로 사용
    # redirect_uri = 'http://localhost:8000/facebook-login/'
    redirect_uri = 'http://melon.dlighter.com/facebook-login/'


    # 아래 엔드포인트에 GET요청을 보냄
    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.get(url, params)
    # 전송받은 결과는 JSON형식의 텍스트. requests가 제공하는 JSON 디코더를 사용해서
    # JSON텍스트를 Python dict로 변환해준다
    response_dict = response.json()
    # 값 출력해보기
    # access_token: EAAXhjYZBChTABANYrACAcZCZCxgrwTYZAIW0j5B5XsSpQBVkWPD8GCYBlwZAyvOAH6w9VdTVzsjVObhtald135JZBWVQwkqLQebfwdE1mbQjFC3vvRYlZBM1i44tAyIyJJWQzVF8bK1UgCOHt1Vd5zi4S7Njfcmziat1rTicC2V4wZDZD
    # token_type: bearer
    # expires_in: 5182104
    for key, value in response_dict.items():
        print(f'{key}: {value}')

    response_dict = response.json()
    for key, value in response_dict.items():
        print('')
        print(f'{key}: {value}')
        print('')

    # -> return 을 명시 안해줘서 오류가 뜨고 대신 shell창에서 값 확인가능

    # return HttpResponse(response_dict['access_token'])
    # -> shell에서 복사하는 것이 힘들어서 이렇게 화면에 바로 출력
    # *참고로 access token 값은 계속 바뀐다.

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
    # return HttpResponse(str(response_dict))


    # {
    # 'id': '796434757212474',
    # 'name': '이한영',
    # 'picture':
    #   {'data': {
    #       'height': 1024,
    #       'is_silhouette': False,
    #       'url': 'https://scontent.xx.fbcdn.net/v/t31.0-1/27164517_781031958752754_5931684880075482184_o.jpg?oh=6997505c279ac83622a253bf1014fd88&oe=5B089210',
    #       'width': 1024}
    #   },
    # 'first_name': '한영',
    # 'last_name': '이'
    # }

    # 애플리케이션 별로 사용자에게 고유한 아이디
    # 아이디별이 아님.
    # 그냥 만들어도 보통은 중복이 안되요.

    facebook_id = response_dict['id']
    name = response_dict['name']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_picture = response_dict['picture']['data']['url']

    # get_or_create를 못씀, createuser해야되서

    # facebook_id가 username인 User가 존재할 경우
    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)
    # 존재하지 않으면 새 유저를 생성

    # 원래 어센티케이티에서 검사했음.
    # 이제 유저를 인증하는 로직을 따로 만들어야함.
    # -> backends.py 만들고 장고문서보러 감.

    else:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
    # 해당 유저를 로그인 시킴
    login(request, user)
    return redirect('index')

