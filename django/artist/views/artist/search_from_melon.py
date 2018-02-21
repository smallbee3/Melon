from django.shortcuts import render


__all__ = (
    'artist_search_from_melon',
)


def artist_search_from_melon(request):
    """
    Template: artist/artist_search_from_melon.html
        form (input[name=keyword]한개, button한개)
    1. form에 주어진 'keyword'로 멜론 사이트의 아티스트 검색 결과를 크롤링
    2. 크롤링 된 검색결과를 적절히 파싱해서 검색 결과 목록을 생성
        -> list내에 dict들을 만드는 형태
        artist_info_list = [
            {'artist_id': 261143, 'name': '아이유', 'url_img_cover': 'http:...'},
            {'artist_id': 261143, 'name': '아이유', 'url_img_cover': 'http:...'},
            {'artist_id': 261143, 'name': '아이유', 'url_img_cover': 'http:...'},
            {'artist_id': 261143, 'name': '아이유', 'url_img_cover': 'http:...'},
        ]
    3. 해당 결과 목록을 템플릿에 출력
        context = {'artist_info_list': artist_info_list}로 전달 후
        템플릿에서 사용
    :param request:
    :return:
    """
    keyword = request.GET.get('keyword')
    context = {}
    if keyword:

        import re
        import requests
        from bs4 import BeautifulSoup

        artist_info_list = []
        URL = 'https://www.melon.com/search/artist/index.htm'
        params = {'q': keyword}
        response = requests.get(URL, params)
        soup = BeautifulSoup(response.text, 'lxml')
        for li in soup.select('div.list_atist12.d_artist_list > ul > li'):
            dl = li.select_one('div.atist_info > dl')
            href = li.select_one('a.thumb').get('href')
            p = re.compile(r"goArtistDetail\('(\d+)'\)")

            artist_id = re.search(p, href).group(1)
            name = dl.select_one('dt:nth-of-type(1) > a').get_text(strip=True)
            url_img_cover = li.select_one('a.thumb img').get('src')

            # 디폴트 이미지의 경우에 이미지가 없는 예외 케이스 처리
            if url_img_cover == 'http://cdnimg.melon.co.kr':
                url_img_cover = 'http://cdnimg.melon.co.kr/resource/image/web/default/noArtist_300_160727.jpg'

            artist_info_list.append({
                'name': name,
                'url_img_cover': url_img_cover,
                'artist_id': artist_id,
            })
        context['artist_info_list'] = artist_info_list
    return render(request, 'artist/artist_search_from_melon.html', context)