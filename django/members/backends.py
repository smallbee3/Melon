from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.base import ContentFile, File

from utils.file import download, get_buffer_ext

User = get_user_model()

import requests

#
# class SettingsBackend:
#     """
#     Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.
#
#     Use the login name and a hash of the password. For example:
#
#     ADMIN_LOGIN = 'admin'
#     ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
#     """
#
#     def authenticate(self, request, username=None, password=None):
#         login_valid = (settings.ADMIN_LOGIN == username)
#         pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
#         if login_valid and pwd_valid:
#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 # Create a new user. There's no need to set a password
#                 # because only the password from settings.py is checked.
#                 user = User(username=username)
#                 user.is_staff = True
#                 user.is_superuser = True
#                 user.save()
#             return user
#         return None
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None


class FacebookBackend:
    CLIENT_ID = settings.FACEBOOK_APP_ID
    CLIENT_SECRET = settings.FACEBOOK_SECRET_CODE
    URL_ACCESS_TOKEN = 'https://graph.facebook.com/v2.12/oauth/access_token'
    URL_ME = 'https://graph.facebook.com/v2.12/me'

    # 바로 아래처럼 facebook_id를 인자로 받는 것으로 작성했다가,
    # 1. 다시 생각해보니 아직 인증되지 않은 유저의 경우
    #   facebook_id가 존재하지 않음.
    # 2. code부터 작업하면 좀 더 많은 내용을 담을 수 있음.
    #    code를 페이스북에 보내서 우리회원인지 확인할 수도 있고
    #    회원아닌경우 get parameter로 전달된 값들로 가입시킬 수도 있음.

    # def authenticate(self, request, facebook_id):

    def authenticate(self, request, code):
        def get_access_token(auth_code):
            """
            유저가 페이스북에서 우리 애플리케이션의 사용에 대해 '승인'한 경우,
            페이스북에서 우리 애플리케이션의 주소(redirect_uri)에 'code'라는 GET parameter로 전해주는
            인증 코드 (auth_code)를 사용해서
            페이스북 GraphAPI에 access_token요청, 결과를 가져와 리턴
            :param auth_code: 유저가 페이스북에 로그인/앱 승인한 결과로 돌아오는 'code' GET parameter
            :return:
            """
            redirect_uri = 'http://localhost:8000/facebook-login/'
            # 아래 엔드포인트에 GET요청을 보냄
            params_access_token = {
                'client_id': self.CLIENT_ID,
                'redirect_uri': redirect_uri,
                'client_secret': self.CLIENT_SECRET,
                'code': auth_code,
            }
            response = requests.get(self.URL_ACCESS_TOKEN, params_access_token)
            # 전송받은 결과는 JSON형식의 텍스트. requests가 제공하는 JSON 디코더를 사용해서
            # JSON텍스트를 Python dict로 변환해준다
            response_dict = response.json()
            return response_dict['access_token']

        def get_user_info(user_access_token):
            """
            User access token을 사용해서
            GraphAPI의 'User'항목을 리턴
                (엔드포인트 'me'를 사용해서 access_token에 해당하는 사용자의 정보를 가져옴)
            :param user_access_token: 정보를 가져올 Facebook User access token
            :return: User정보 (dict)
            """
            params = {
                'access_token': user_access_token,
                'fields': ','.join([
                    'id',
                    'name',
                    'picture.width(2500)',
                    'first_name',
                    'last_name',
                ])
            }
            response = requests.get(self.URL_ME, params)
            response_dict = response.json()
            return response_dict

        try:    # -> 아래 인증과정에서 오류가 발생할 경우
                #    None을 리턴할 수 있도록.
            access_token = get_access_token(code)
            user_info = get_user_info(access_token)

            facebook_id = user_info['id']
            name = user_info['name']
            first_name = user_info['first_name']
            last_name = user_info['last_name']
            url_picture = user_info['picture']['data']['url']

            try:    # -> 회원가입되지 않은 유저의 경우 예외처리
                user = User.objects.get(username=facebook_id)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=facebook_id,
                    first_name=first_name,
                    last_name=last_name,
                    # img_profile=,
                )

                # file_name = '{album_id}.{ext}'.format(
                #     album_id=album_id,
                #     ext=get_buffer_ext(temp_file),
                # )
                # 방법1 - 지우고 다시 만들기
                # if album.img_cover:
                #     album.img_cover.delete()

            # 사진이 없을 때만 저장하는 것으로 간단하게 실습.
            if not user.img_profile:
                temp_file = download(url_picture)
                ext = get_buffer_ext(temp_file)
                user.img_profile.save(f'{user.pk}.{ext}', File(temp_file))
            return user

            # binary_data = request.get(url_picture)
            # user.img_profile.save(facebook_id, ContentFile(binary_data))

        except Exception:
            return None

    # "왜 만드는지는 정확히 모르겠는데 필수로 만들라고 해서"
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None