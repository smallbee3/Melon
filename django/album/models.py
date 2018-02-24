from datetime import datetime

from django.core.files import File
from django.db import models

from artist.models import Artist
from crawler.album import album_detail_crawler
from utils.file import get_buffer_ext, download


def dynamic_album_cover_path(instance, filename):
    # return f'album/{instance.title}-{instance.album_id}/album_cover.png'
    return f'album/{instance.title}-{instance.album_id}/{filename}'


class AlbumManager(models.Manager):

    def update_or_create_from_melon(self, album_id):
        result = album_detail_crawler(album_id)

        album_title = result.get('album_title')
        # album_cover = result.get('album_cover')
        album_cover_url = result.get('album_cover_url')
        rel_date = result.get('rel_date')

        album, album_created = self.update_or_create(
            album_id=album_id,
            defaults={
                'title': album_title,
                # 'img_cover': album_cover,
                'release_date': datetime.strptime(rel_date, '%Y.%m.%d'),
            }
        )

        temp_file = download(album_cover_url)
        file_name = '{album_id}.{ext}'.format(
            album_id=album_id,
            ext=get_buffer_ext(temp_file),
        )
        # 방법1 - 지우고 다시 만들기
        if album.img_cover:
            album.img_cover.delete()
        album.img_cover.save(file_name, File(temp_file))



        return album, album_created

    # def get_or_create_from_melon(self, album_id):
    #     result = album_detail_crawler(album_id)
    #
    #     album_title = result.get('album_title')
    #     album_cover = result.get('album_cover')
    #     rel_date = result.get('rel_date')
    #
    #     album, album_created = self.get_or_create(
    #         album_id=album_id,
    #         defaults={
    #             'title': album_title,
    #             'img_cover': album_cover,
    #             'release_date': datetime.strptime(rel_date, '%Y.%m.%d'),
    #         }
    #     )
    #     return album, album_created


class Album(models.Model): # -> 모델을 상속받는 모델 클래스
    album_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    title = models.CharField('앨범명', max_length=255)
    img_cover = models.ImageField(
        '커버 이미지',
        # upload_to='album',
        upload_to=dynamic_album_cover_path,
        blank=True,
    )
    # artists = models.ManyToManyField(Artist, verbose_name='아티스트 목록')
    # # 수업시간

    # song은 Song 클래스에서 다대일(ForeignKey)로 참조
    release_date = models.DateField('발매일', blank=True, null=True)

    # genre = models.CharField('장르', max_length=100, blank=True)
    # 장르는 가지고 있는 노래들에서 가져오기
    @property
    def genre(self):
        return ','.join(self.song_set.values_list('genre', flat=True).distinct())

    def __str__(self):
        # return '{title} [{artists}]'.format(
        #     title=self.title,
        #     artists=', '.join(self.artists.values_list('name', flat=True))
        # )
        return f'앨범명: {self.title}'

    objects = AlbumManager()

# 얘가 아티스트랑 연결. 하위개념이 앨범, 상위개념이 아티스트
# 그러면 관계 정의필드에서 하위필드.


# 소스랑 타겟
# 소스가 아티스트고 타겟이 앨범이 되는데

# 송은 앨범이랑 1대 다 관계
# 한 노래가 다른 앨범에 들어가 있지는 않음.

# 정규앨범만 치면 한 노래는 하나에만 들어있음.

# 한 앨범에는 노래가 여러개 -> 1대 다