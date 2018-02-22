import re
from django.db import models


# 밖에 있는 이유는 클래스 안에 넣어도 상관은 없기도 하고.
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

    # print(filename)
    filename = re.search(r'(.*)\.(png|jpg|jpeg|gif)', filename).group(1)
# print(filename)
    return f'artist/{instance.name}-{instance.melon_id}/{filename}_img.png'



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
    # 수업시간


    # member = models.CharField(
    #     '멤버',
    #     max_length=100,
    #     blank=True,
    # )
    # agency = models.CharField(
    #     '소속사',
    #     max_length=50,
    #     blank=True,
    #     null=True,
    # )




    def __str__(self):
        return f'{self.name} {self.birth_date}'