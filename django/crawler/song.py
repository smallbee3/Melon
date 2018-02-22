import re


def song_list_crawler(q):

    import requests
    from bs4 import BeautifulSoup
    url = 'https://www.melon.com/search/song/index.htm'
    params = {
        'q': q,
        'section': 'song',
    }

    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')

    # select는 모든 값을 찾아 리스트로 반환, find_all과 비슷한 역할
    tr_list = soup.select('form#frm_defaultList table > tbody > tr')
    # tr = soup.find('form', id='frm_defaultList').find('table').find('tbody').find_all('tr')

    result = []
    for tr in tr_list:
        # <a href="javascript:searchLog('web_song','SONG','SO','빨간맛','30512671');melon.play.playSong('26020103',30512671);" class="fc_gray" title="빨간 맛 (Red Flavor)">빨간 맛 (Red Flavor)</a>
        # song_id = re.search(r"searchLog\(.*'(\d+)'\)", tr.select_one('td:nth-of-type(3) a.fc_gray').get('href')).group(1)
        song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
        # title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)

        # 2/22 수업에서 제목에 회색처리 된 곳 예외처리코드 추가
        if tr.select_one('td:nth-of-type(3) a.fc_gray'):
            title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
        else:
            title = tr.select_one('td:nth-of-type(3) > div > div > span').get_text(strip=True)


        artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(
            strip=True)
        album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

        # print(f'song_id: {song_id}')
        # print('')
        # print(f'title: {title}')
        # print('')
        # print(f'artist {artist}')
        # print('')
        # print(f'album: {album}')

        result.append({
            'song_id': song_id,
            'title': title,
            'artist': artist,
            'album': album,
        })
    return result


def song_detail_crawler(song_id):

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
    # print(zip(it, it))
    ##############################################
    # zip은 안에 iterable한 객체를 동시에 가져와서 묶는게 아니라
    # 순서대로 호출해서 가져오기때문에
    # iterator를 동시에 묶을 때는
    # 'iterator의 자신의 호출된 상태를 기억하는 특성'
    # 때문에 번갈아서 묶이는 것처럼 보이게 된다.
    ##############################################

    # print(type(it)) -> <class 'list_iterator'>
    description_dict = dict(zip(it, it))
    # print(description_dict)

    # value가 없을 수도 있으므로 get()으로 넣어준다.
    # album = description_dict.get('앨범')
    # release_date = description_dict.get('발매일')
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

    # print('')
    # print(f'album_id: {album_id}')
    # print('')

    # 5) melon_id (artist_id) 가져오기 [2/22 수업실습]
    melon_id_str = div_entry.select_one('div.artist > a').get('href')
    melon_id = re.search(".*'(.*)'[)]", melon_id_str).group(1)


    result_dict = {
        'title': title,
        'genre': genre,
        'lyrics': lyrics,

        'album_id': album_id,

    # 5) melon_id (artist_id) 가져오기 [2/22 수업실습]
        'melon_id': melon_id,
    }

    return result_dict