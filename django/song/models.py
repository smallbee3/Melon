from datetime import datetime

import re
from django.utils import timezone


from django.db import models

from album.models import Album
from artist.models import Artist

# Artist
#   - Album
#       - Song
#       - Song
#       - Song
from crawler.album import album_detail_crawler


class SongManager(models.Manager):

    def update_or_create_from_melon_id(self, song_id):

        import requests
        from bs4 import BeautifulSoup, NavigableString
        url = f'https://www.melon.com/song/detail.htm'
        params = {
            'songId': song_id,
        }
        response = requests.get(url, params)
        source = response.text
        soup = BeautifulSoup(source, 'lxml')

        # 1) title
        div_entry = soup.find('div', class_='entry')
        title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()

        # 2) genre (Description list)
        dl = div_entry.find('div', class_='meta').find('dl')
        # isinstance(인스턴스, 클래스(타입))
        # items = ['앨범', '앨범명', '발매일', '발매일값', '장르', '장르값']
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        # print(type(items)) -> <class 'list'>
        # print(items)

        it = iter(items)
        description_dict = dict(zip(it, it))
        genre = description_dict.get('장르')

        # 3) lyrics - 첫번째 주석처리와 띄어쓰기 문제해결
        div_lyrics = soup.find('div', id='d_video_summary')

        if div_lyrics:
            lyrics_list = []
            for item in div_lyrics:
                if item.name == 'br':
                    lyrics_list.append('\n')
                elif type(item) is NavigableString:
                    lyrics_list.append(item.strip())
            lyrics = ''.join(lyrics_list)
        else:
            lyrics = ''

        # 4) album_id - Song을 DB에 저장할 때 Album도 같이 생성해주기 위함.
        #               참고로 Song은 Album을 ForeignKey로 가짐.
        p = re.compile(r".*goAlbumDetail[(]'(\d+)'[)]")

        first_dd = dl.find('dd')
        album_id = p.search(str(first_dd)).group(1)


        # # 5) melon_id (artist_id) 가져오기 [2/22 수업실습]
        # melon_id_str = div_entry.select_one('div.artist > a').get('href')
        # melon_id = re.search(".*'(.*)'[)]", melon_id_str).group(1)



        album_info = album_detail_crawler(album_id)
        album, created = Album.objects.get_or_create(
            album_id=album_id,
            defaults={
                "title": album_info.get("album_title"),
                "img_cover": album_info.get('album_cover'),
                "release_date": datetime.strptime(album_info.get('rel_date'), '%Y.%m.%d')
            }
        )

        song, song_created = self.update_or_create(
            song_id=song_id,
            defaults={
                'title': title,
                'genre': genre,
                'lyrics': lyrics,
                'album': album,
            }
        )

        return song, song_created




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


    # 2/22
    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록',
        blank=True,
    )

    # 아래 프로퍼티 겹쳐서 없애야함




    title = models.CharField('곡 제목', max_length=100)

    genre = models.CharField('장르', max_length=100, blank=True)

    lyrics = models.TextField('가사', blank=True)



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

        # 2017.01.15
        # return self.album.release_date

    # 이전에 사용했던 방식.
    # datetime.strftime(
    #     # timezone.make_naive(self.created_date),
    #     timezone.localtime(self.created_date),
    #     '%Y.%m.%d'),



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

    objects = SongManager()


# class ArtistSong(models.Model):
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     song = models.ForeignKey(Song, on_delete=models.CASCADE)
#     demo_date = models.DateTimeField(null=True) # -> 초기 데이터 없어서 에러남.
#     # producer = models.ForeignKey() -> through_field해야되서 일단 뺌.
#
#     def __str__(self):
#         return f'{self.artist} - {self.song}'