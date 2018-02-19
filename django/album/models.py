from django.db import models

from artist.models import Artist


class Album(models.Model): # -> 모델을 상속받는 모델 클래스
    title = models.CharField('앨범명', max_length=255)
    img_cover = models.ImageField(
        '커버 이미지',
        upload_to='album',
        blank=True,
    )
    artists = models.ManyToManyField(Artist, verbose_name='아티스트 목록')
    # 수업시간

    # song은 Song 클래스에서 다대일(ForeignKey)로 참조
    release_date = models.DateField('발매일', blank=True, null=True)

    # genre = models.CharField('장르', max_length=100, blank=True)
    # 장르는 가지고 있는 노래들에서 가져오기
    @property
    def genre(self):
        return ','.join(self.song_set.values_list('genre', flat=True).distinct())

    def __str__(self):
        # return f'앨범명: {self.title}'
        return '{title} [{artists}]'.format(
            title=self.title,
            artists=', '.join(self.artists.values_list('name', flat=True))
        )


# 얘가 아티스트랑 연결. 하위개념이 앨범, 상위개념이 아티스트
# 그러면 관계 정의필드에서 하위필드.


# 소스랑 타겟
# 소스가 아티스트고 타겟이 앨범이 되는데

# 송은 앨범이랑 1대 다 관계
# 한 노래가 다른 앨범에 들어가 있지는 않음.

# 정규앨범만 치면 한 노래는 하나에만 들어있음.

# 한 앨범에는 노래가 여러개 -> 1대 다
