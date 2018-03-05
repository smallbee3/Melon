"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from config import views
from members.views import login_view, logout_view, signup_view, facebook_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('facebook-login/', facebook_login, name='facebook-login'),

    path('artist/', include('artist.urls')),
    path('song/', include('song.urls')),
    path('album/', include('album.urls')),

    path('video/', include('video.urls')),
    path('sms/', include('sms.urls')),
    path('emails/', include('emails.urls')),

]

# settings.MEDIA_URL('/media/')로 시작하는 요청은
# document_root인 settings.MEDIA_ROOT폴더(ROOT_DIR/.media)
# 에서 파일을 찾아 리턴해준다
# -> 개발환경에서만 작동하지 실제 운영환경에서는 사용하지 않음.
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
