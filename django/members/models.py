from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # User클래스를 정의
    # INSTALLED_APPS에 members application추가
    # AUTH_USER_MODEL 정의 (AppName.ModelClassName)
    # 모든 application들의 migrations폴더내의 Migration파일 전부 삭제
    # makemigrations -> migrate

    # 데이터베이스에 member_user 테이블이 생성되었는지 확인

    def toggle_like_artist(self, artist):
        # if self.like_artist_info_list.filter(like_users=artist).exists():
        #     self.like_artist_info_list.filter(like_users=artist).delete()
        # else:
        #     self.like_artist_info_list.create(
        #         artist=artist,
        #     )

        like, like_created = self.like_artist_info_list.get_or_create(artist=artist)
        if not like_created:
            like.delete()
        return like_created

# -> appname이랑 모델 안의 클래스가 이름이 같아야 한다고 착각하고 한 뻘짓.
# class Members(User):
#     pass

