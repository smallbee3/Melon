import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile


def album_detail_crawler(album_id):

    url = f'https://www.melon.com/album/detail.htm'
    params = {
        'albumId': album_id,
    }

    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')

    # 앨범 제목
    album_title = soup.find('div', class_="song_name").strong.next_sibling.strip()

    # 앨범 사진 - 이곳에서 바로 저장
    album_cover_url = soup.find('a', id="d_album_org").img.get('src')
    binary_data = requests.get(album_cover_url).content
    album_cover = ContentFile(binary_data, name="album_cover.png")

    # 앨범 발매일
    meta = soup.find('dl', class_="list")
    rel_date = meta.find("dd").get_text(strip=True)

    result_dict = {
        'album_title': album_title,
        'album_cover': album_cover,
        'rel_date': rel_date,
    }
    return result_dict


# 크롤러 동작 실험
# album_detail_crawler(10077879)