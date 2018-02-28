from django.conf import settings
from django.db import models

# 밖에 있는 이유는 클래스 안에 넣어도 상관은 없기도 하고.
from artist.models.managers import ArtistManager
from video.models import Video


def dynamic_profile_img_path(instance, filename):
    # return을 원하는 디렉토리 네임.
    # 인스턴스랑 파일네임을 받도록 하고, 인스턴스는 저장하는 파일 객체,

    # 방법1 - instance 사용
    # return f'artist/{instance.name}/profile_img.png'

    # 방법2 - instance + filename 사용
    # return f'artist/{instance.name}/{filename}'

    # 방법3 - 확장자 없는게 문제될 수도 있어서
    # return f'artist/{instance.name}/{filename}_img.png'

    # 방법 4 - 예를 pk값으로 주면 됨.
    # return f'artist/{instance.pk}/{filename}_img.png'
    # -> none으로 나옴

    # 이미지 저장되는데는 인스턴스의 pk가 부여안된상태에서 이미지 파일을
    # 저장업데이트를 하면 되요. 왜냐하면 pk값이 부여받은 상태에서 이미지 파일이 저장
    # 저장되는 순서가 필드를 다 저장을 하고 인스턴스를 저장.
    # 이미지 필드가 저장되는 순간에는 인스턴스가 저장되는 ㅏㄴ된.
    # db에 저장이 안된상태에서 이미지 필드에 저장을 하고. 그 다음에
    # (아마 밸리데이션때문에 그런것같은데) 반대로 하면 이상하잖아요.
    # 이상한 파일을 먼저 인스턴스를 만드는게 안되잖아요.

    # 방법 4-2 - 그런데 우리가 만드는 프로젝트는 이런게 없잖아요.

    # pk를 갖기위한 일종의 편법
    # 저장되는 순서가
    # (저장 -> pre_save -> save -> post_save -> 끝)
    #       여기서 시그널을 잡아서
    #       이미지 필드를 none으로 저장을 하는 거에요.
    #       이미지 필드에 아무것도 없이 디비에 저장이 되겠죠.
    #       post_save에 저장을 하는거에요.
    # -> validation(유효성 검사) 없이 일단 none으로 만들고 보니까
    #    해당 내용이 중요한 내용일 경우 사용하면 문제가 발생할 수 있음.

    # 방법 5 - pk 대신 melon_id를 사용

    # return f'artist/{instance.name}-{instance.melon_id}/profile_img.png'

    # 정규표현식으로 원본 파일명에서 확장자를 떼는 코드인데
    # 원래 확장명을 버리고 .png로 통일하는게 꼭 필요하지 않은이상
    # 이상적인 코드라고 보기 힘듦.
    # filename = re.search(r'(.*)\.(png|jpg|jpeg|gif)', filename).group(1)
    # return f'artist/{instance.name}-{instance.melon_id}/{filename}_img.png'

    return f'artist/{instance.name}-{instance.melon_id}/{filename}'

    # return f'artist/{instance.name}-{instance.melon_id}/profile_img.png'



class Artist(models.Model):
    BLOOD_TYPE_A = 'a'
    BLOOD_TYPE_B = 'b'
    BLOOD_TYPE_O = 'o'
    BLOOD_TYPE_AB = 'c'
    BLOOD_TYPE_OTHER = 'x'

    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_AB, 'AB형'),
        (BLOOD_TYPE_OTHER, '기타'),
    )
    melon_id = models.CharField(
        '멜론 Artist ID',
        max_length=20,
        blank=True,
        null=True,
        unique=True,

        # 1)
        # unique=True걸기전에 null=True만 허용하기 위해
        # make migration, migrate하고 shell에서
        # 값을 바꿔줄 것.

        # Artist.objects.filter(melon_id='').update(melon_id=None)

        # 2) 그 다음에
        # unique=True하고
        # migration / migrate
    )

    img_profile = models.ImageField(
        '프로필 이미지',
        # upload_to='artist',
        upload_to=dynamic_profile_img_path,
        blank=True,
    )
    name = models.CharField(
        '이름',
        max_length=50,
    )
    real_name = models.CharField(
        '본명',
        max_length=30,
        blank=True,
    )
    nationality = models.CharField(
        '국적',
        max_length=50,
        blank=True,
    )
    birth_date = models.DateField(
        '생년월일',
        blank=True,
        null=True,
    )
    constellation = models.CharField(
        '별자리',
        max_length=30,
        blank=True,
    )
    blood_type = models.CharField(
        '혈액형',
        max_length=1,
        choices=CHOICES_BLOOD_TYPE,
        blank=True,
    )
    intro = models.TextField(
        '소개',
        blank=True,
    )

    # 2/26 수업시간에 '좋아요' 기능구현 위해 추가
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ArtistLike', # 밑에선언되어있어서 문자로 써야함.
        related_name='like_artists',
        blank=True,
    )

    # 2/27 YouTube 관련 과제
    videos = models.ManyToManyField(
        Video,
        # blank=True,
    )

    # 위에서 열심히 만든 Manager를 object에 할당하기.
    objects = ArtistManager()

    def __str__(self):
        return f'{self.name} {self.birth_date}'

    def toggle_like_user(self, user):

        """
        자신의 like_users에 주어진 user가 존재하지 않으면
            like_users에 추가한다
        이미 존재할 경우에는 없앤다
        :param user:
        :return:
        """
        # 나 - 하다가 실패
        # self.like_user_info_list.create(user=user)


        # 1단계
        # # 자신이 artist이며, 주어진 user와의 ArtistLike의 QuerySet
        # query = ArtistLike.objects.filter(artist=self, user=user)
        # # QuerySet이 존재할 경우
        # if query.exists():
        #     # 지워주고 False반환
        #     query.delete()
        #     return False
        # # QuerySet이 존재하지 않을 경우
        # else:
        #     # 새로 ArtistLike를 생성하고 True반환
        #     ArtistLike.objects.create(artist=self, user=user)
        #     return True

        # 2단계
        # 자신이 'artist'이며 user가 주어진 user인 ArtistLike를 가져오거나 없으면 생성
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        # 만약 이미 있었을 경우 (새로 생성되지 않았을 경우)
        if not like_created:
            # Like를 지워줌
            like.delete()
        # 생성여부를 반환 (Toggle후 현재 상태에 대한 True/False와 같은 결과)
        return like_created
