from datetime import datetime

from django.conf import settings
from django.db import models

from album.models import Album
# from artist.models import Artist

# Artist
#   - Album
#       - Song
#       - Song
#       - Song
from artist.models.artist import Artist
from crawler.song import song_detail_crawler


# 2/22 목요일 폭풍과제 - Album 사진 저장, Album manager 구현
class SongManager(models.Manager):

    def update_or_create_from_melon_id(self, song_id):
        """
        song_id에 해당하는 Song정보를 멜론사이트에서 가져와 update_or_create를 실행
        이 때, 해당 Song의 Artist정보도 가져와 ArtistManager.update_or_create_from_melon도 실행
         그리고 해당 Song의 Album정보도 가져와서 AlbumManager.update_or_create_from_melon도 실행
            -> Album의 커버이미지도 저장해야 함
        :param song_id: 멜론 사이트에서의 곡 고유 ID
        :return: (Song instance, Bool(Song created))
        """
        result = song_detail_crawler(song_id)


        # 1) 아티스트 생성
        artist_id = result.get('melon_id')
        artist, artist_created = Artist.objects.update_or_create_from_melon(artist_id)


        # 2) 앨범 생성
        album_id = result.get('album_id')
        album, _ = Album.objects.update_or_create_from_melon(album_id)


        # 3) 음악 생성
        title = result.get('title')
        genre = result.get('genre')
        lyrics = result.get('lyrics')
        song, song_created = self.update_or_create(
            song_id=song_id,
            defaults={
                'title': title,
                'genre': genre,
                'lyrics': lyrics,

        # 4) 음악에 앨범 연결
                'album': album,
            }
        )

        # 5) 음악에 아티스트 연결
        song.artists.add(artist)
        # 생성된 Song의 artists필드(MTM)에 연결된 Artist를 추가


        # return song, song_created
        # 여기서 return을 할 필요가 없어짐.


class Song(models.Model):

    song_id = models.CharField(max_length=50, blank=True, null=True, unique=True)

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='앨범',
        # blank=True, # -> 강남스타일 때문에 큰코 다친 후 주석처리함.
        null=True,
    )     # through_fields=('artist', 'song')) # (상위개념, 하위개념)
          # -> 한노래에 가수 여러명, 가수가 노래 여러개
    # 보통 중간자모델이 아래에 있어서 ''string으로 해주는 것.


    # 2/22 수업 중에 모델 형태를 같이 변경함.
    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록',
        blank=True,
        # Song <-> Artist는 MTM관계이고 CASCADE가 설정 안되어있으므로
        # Album이 지워질 때 Song은 지워지지만 (Song이 지워질때 Album은 지워지지만 X)
        # artist는 남아있음.
    )
    title = models.CharField(
        '곡 제목',
        max_length=100,
    )
    genre = models.CharField(
        '장르',
        max_length=100,
    )
    lyrics = models.TextField(
        '가사',
        blank=True,
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='SongLike',
        related_name='like_songs',
        blank=True,
    )

    # 위에 변경한 artists와 프로퍼티 겹쳐서 없애야함
    # @property
    # def artists(self):
    #     # self.album에 속한 전체 Artist의 QuerySet리턴
    #     return self.album.artists.all()

    @property
    def release_date(self):
        # self.album의 release_date를 리턴
        return self.album.release_date

    @property
    def formatted_release_date(self):
        return self.album.release_date.strftime('%Y.%m.%d')

    objects = SongManager()

    def __str__(self):
        # 가수명 - 곡제목 (앨범명)
        # TWICE(트와이스) - Heart Shaker (Merry & Happy)
        # 휘성, 김태우 - 호호호빵 (호호호빵)
        #  artists는 self.album의 속성
        if self.album:
            return '{title} ({album})'.format(
            # return '{artists} - {title} ({album})'.format(
                # artists=', '.join(self.album.artists.values_list('name', flat=True)),
                title=self.title,
                album=self.album.title,
            )
        else:
            return self.title
            # 강남스타일 사건(앨범이 없어서 위에 출력에서 에러)때문에
            # if self.album으로 분기함

    def toggle_like_user(self, user):

        like, like_created = self.like_user_info_list.get_or_create(user=user)
        if not like_created:
            like.delete()
        return like_created


class SongLike(models.Model):

    song = models.ForeignKey(
        Song,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_song_info_list',
        on_delete=models.CASCADE,
    )

    created_data = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            ('song', 'user'),
        )

    def __str__(self):
        return 'SongLike (User: {user}, Song: {song}, Created: {created})'.format(
            user=self.user.username,
            song=self.song.title,
            created=datetime.strftime(self.created_data, '%y.%m.%d')
        )

# class ArtistSong(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     song = models.ForeignKey(Song, on_delete=models.CASCADE)
#     demo_date = models.DateTimeField(null=True) # -> 초기 데이터 없어서 에러남.
#     # producer = models.ForeignKey() -> through_field해야되서 일단 뺌.
#
#     def __str__(self):
#         return f'{self.artist} - {self.song}'