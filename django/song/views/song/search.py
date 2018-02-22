from typing import NamedTuple
from collections import namedtuple

from django.db.models import Q
from django.shortcuts import render

from ...models import Song


def song_search(request):
    """
    사용할 URL: song/search/
    사용할 Template: templates/song/song_search.html
        form안에
            input한개, button한개 배치
    1. song/urls.py에 URL작성
    2. templates/song/song_search.html작성
        {% extends %} 사용할 것
        form배치 후 method는 POST, {% csrf_token %}배치
    3. 이 함수에서 return render(...)
        *아직 context는 사용하지 않음
    - GET, POST분기
    1. input의 name을 keyword로 지정
    2. 이 함수를 request.method가 'GET'일 때와 'POST'일 때로 분기
    3. request.method가 'POST'일 때
        request.POST dict의 'keyword'키에 해당하는 값을
        HttpResponse로 출력
    4. request.method가 'GET'일 때
        이전에 하던 템플릿 출력을 유지
    - Query filter로 검색하기
    1. keyword가 자신의 'title'에 포함되는 Song쿼리셋 생성
    2.  위 쿼리셋을 'songs'변수에 할당
    3. context dict를 만들고 'songs'키에 songs변수를 할당
    4. render의 3번째 인수로 context를 전달
    5. template에 전달된 'songs'를 출력
        song_search.html을 그대로 사용
    :param request:
    :return:
    """

    # 2. 중복되는 render함수 합치기
    '''
    02/19 과제
    # Song과 연결된 Artist의 name에 keyword가 포함되는 경우
    # Song과 연결된 Album의 title에 keyword가 포함되는 경우
    # Song의 title에 keyword가 포함되는 경우
      를 모두 포함(or -> Q object)하는 쿼리셋을 'songs'에 할당

    songs_from_artists
    songs_from_albums
    songs_from_title
     위 세 변수에 위의 조건 3개에 부합하는 쿼리셋을 각각 전달
     세 변수를 이용해 검색 결과를 3단으로 분리해서 출력
     -> 아티스트로 검색한 노래 결과, 앨범으로 검색한 노래 결과, 제목으로 검색한 노래 결과
    '''
    # print(request.GET)
    # print(type(request.GET))
    # print(request.GET.get('keyword'))

    # print(request.GET['keyword'])
    # -> GET방식에서 'keyword'가 없는상태로 접근하면
    #    MultiValueDictKeyError가 발생
    #    ex) 주소창에서 엔터치고 들어가는 것


    keyword = request.GET.get('keyword')
    #######################################
    # keyword = request.GET['keyword']
    # -> 아래 줄에서 되고 여기서 안되는것은 바로 아래의 if문으로 검사하기 때문?
    # 이 아님. 아래줄에서도 주소창으로 get방식으로 접근하면 'keyword'가 없기 때문에
    # 같은 에러가 발생.
    #######################################

    # if request.method == 'GET': #'get'으로 하면 안됨.
    #   keyword = request.GET['keyword'].strip() # -> 양쪽의 공백이 있을 경우

    context = {
        'song_infos': [],
    }

    if keyword:  # -> 공백(엔터) 값이 아닐 경우
                 #   (이게 없으면 ''가 모든 song과 매치되어서 모든 song이 출력됨)
        # return HttpResponse(keyword)

        # 2/19 수업시간 마지막 부분에 'Q'와 '|' 실습 (녹화안됨)
        # songs = Song.objects.filter(
        #     Q(album__artists__name__contains=keyword) |
        #     Q(album__title__contains=keyword) |
        #     Q(title__contains=keyword)
        # ).distinct()
            # context = {
            #     'songs': songs,
            # }
            # 위 방법도 가능하지만 먼저 생성한 context에 값만 넣어주도록
            # context['songs'] = songs
    #     return render(request, 'song/song_search.html', context)
    # else:
    #     return render(request, 'song/song_search.html')



        # 아래 부분은 4단계에서 'Q'를 사용하면서 필요없어짐
        #############################################
        #Song과 연결된 Artist의 name에 keyword가 포함되는 경우
        # songs_from_artists = Song.objects.filter(
        #     album__artists__name__contains=keyword
        # )
        # # context['songs_from_artists'] = songs_from_artists
        #
        # # Song과 연결된 Album의 title에 keyword가 포함되는 경우
        # songs_from_albums = Song.objects.filter(
        #     album__title__contains=keyword
        # )
        # # context['songs_from_albums'] = songs_from_albums
        #
        # # Song의 title에 keyword가 포함되는 경우
        # songs_from_title = Song.objects.filter(
        #     title__contains=keyword
        # )
        # context['songs_from_title'] = songs_from_title
        #############################################


        # 0단계 - '리스트'로 시도하다 실패 because of 템플릿언어 리스트
        #
        # items = []
        # items.append([songs_from_artists, '아티스트명'])
        # items.append([songs_from_albums, '앨범명'])
        # items.append([songs_from_title, '노래제목'])


        # 1단계 - '딕셔너리'로 수업시간 실습
        # context['song_infos'].append({
        #     'type': '아티스트명',
        #     'songs': songs_from_artists,
        # })
        # context['song_infos'].append({
        #     'type': '앨범명',
        #     'songs': songs_from_albums,
        # })
        # context['song_infos'].append({
        #     'type': '노래제목',
        #     'songs': songs_from_title,
        # })


        # 2단계 - zip을 사용해서 깔끔하게 해보기 실습
        # type_list = ('아티스트명', '앨범명', '노래제목')
        # songs_list = (songs_from_artists, songs_from_albums, songs_from_title)
        # items = zip(type_list, songs_list)
        #
        # for types, songs in items:
        #     context['song_infos'].append({
        #         'type': types,
        #         'songs': songs,
        #     })


        # 3단계 - zip쓸 때 길어지면 알아보기 힘드니 좀 더 보기 쉽게
        # song_infos = (
        #     ('아티스트명', songs_from_artists),
        #     ('앨범명', songs_from_albums),
        #     ('노래제목', songs_from_title),
        # )
        # for type, songs in song_infos:
        #     context['song_infos'].append({
        #         'type': type,
        #         'songs': songs,
        #     })


        # 4단계 - 어제 배운 "Q" objects를 써보기
        # song_infos = (
        #     ('아티스트명', Q(album__artists__name__contains=keyword)),
        #     ('앨범명', Q(album__title__contains=keyword)),
        #     ('노래제목', Q(title__contains=keyword)),
        # )
        # for type, q in song_infos:
        #     context['song_infos'].append({
        #         'type': type,
        #         'songs': Song.objects.filter(q),
        #     })


        # 5-1단계 - 튜플에 이름 붙이기
        # SongInfo = namedtuple('SongInfo', ['type', 'q'])


        # 5-2단계 - 바로 위에 '튜플에 이름 붙이기'는 것에 타입까지 명시
        # https://docs.python.org/3/library/typing.html#typing.NamedTuple
        class SongInfo(NamedTuple):
            type: str
            q: Q

        song_infos = (
            SongInfo(
                # type=123, -> 위의 class형 NamedTuple은
                #               개발툴에서 디버깅을 할 수 있도록 함.
                #               에러가 아닌, 워닝을 띄워줌.
                type='아티스트명',
                q=Q(album__artists__name__contains=keyword)),
            SongInfo(
                type='앨범명',
                q=Q(album__title__contains=keyword)),
            SongInfo(
                type='노래제목',
                q=Q(title__contains=keyword)),
        )
        for types, q in song_infos:
            context['song_infos'].append({
                'types': types,
                'songs': Song.objects.filter(q),
            })


# 2. 중복되는 render함수 합치기
    # 만약 method가 POST였다면 context에 'songs'가 채워진 상태,
    # GET이면 빈 상태로 render실행
    return render(request, 'song/song_search.html', context)

