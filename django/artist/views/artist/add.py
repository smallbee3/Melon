from django.shortcuts import redirect, render

from ...forms import AritstForm


__all__ = (
    'artist_add',
)

# def artist_add(request):
    # HTML에 Artist클래스가 받을 수 있는 모든 input을 구현
    #   img_profile은 제외
    # method가 POST면 request.POST에서 해당 데이터 처리
    #   새 Artist객체를 만들고 artist_list로 이동
    # method가 GET이면 artist_add.html을 표시

    # ** 생년월일은 YYYY-MM-DD 형식으로 받음
    #      이후 datetime.strptime을 사용해서 date객체로 변환

    # 1. artist_add.html 작성
    # 2. url과 연결, /artist/add/ 에 매핑
    # 3. GET요청시 잘 되는지 확인
    # 4. form method설정 후 POST요청시를 artist_add() view에서 분기
    # 5. POST요청의 값이 request.POST에 잘 오는지 확인
    #       name값만 받아서 name만 갖는 Artist를 먼저 생성
    #       성공 시 나머지 값들을 하나씩 적용해보기
    # 6. request.POST에 담긴 값을 사용해 Artist인스턴스 생성
    # 7. 생성 완료 후 'artist:artist-list' URL name에 해당하는 view로 이동

    # 1. artist/artist_add.html에 Artist_add다 라는 내용만 표시
    #   url, view를 서로 연결
    #   artist/add/ URL사용

    # 2. aritst_add.html에 form을 하나 생성
    #       input은 name이 'name'인 요소 한개만 생성
    #       POST방식으로 전송 후, 전달받은 'name'값을 바로 HttpResponse로 보여주기

    # 3. 전송받은 name을 이용해서 Artist를 생성
    #       이후 'artist:artist-list'로 redirect
    #
    # if request.method == 'POST':
    #     name = request.POST['name']
    #     Artist.objects.create(
    #         name=name,
    #     )
    #     return redirect('artist:artist-list')
    # else:
    #     return render(request, 'artist/artist_add.html')


# def artist_add(request):
#     if request.method == 'POST':
#
#         name = request.POST['name']
#         real_name = request.POST['real_name']
#         nationality = request.POST['nationality']
#         constellation = request.POST['constellation']
#         blood_type = request.POST['blood_type']
#         intro = request.POST['intro']
#
#         if request.POST['birth_date']:
#             birthday_text = request.POST['birth_date']
#             birth_date = datetime.strptime(birthday_text, '%Y-%m-%d')
#         else:
#             birth_date = None
#         Artist.objects.create(
#             name=name,
#             real_name=real_name,
#             nationality=nationality,
#             birth_date=birth_date,
#             constellation=constellation,
#             blood_type=blood_type,
#         )
#         return redirect('artist:artist-list')
#     else:
#         return render(request, 'artist/artist_add.html')

def artist_add(request):
    if request.method == 'POST':
        """
        multipart/form-data로 전달된 파일은
        request.FILES 속성에 들어있음
        boundform을 만들 때, request.POST와 request.FILES를 전부 전달
        """
        form = AritstForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # -> 아티스트 객체를 저장.
            #    굳이 풀어서 하자면 아래처럼
            #    cleaned_data에서 꺼내서
            #    Artist.objects.create하는 과정이됨

            # # melon_id = form.cleaned_data['melon_id']
            # img_profile = form.cleaned_data['img_profile']
            # name = form.cleaned_data['name']
            # real_name = form.cleaned_data['real_name']
            # nationality = form.cleaned_data['nationality']
            # birth_date = form.cleaned_data['birth_date']
            # constellation = form.cleaned_data['constellation']
            # blood_type = form.cleaned_data['blood_type']
            # intro = form.cleaned_data['intro']
            #
            # # if form.cleaned_data['birth_date']:
            # #     birthday_text = form.cleaned_data['birth_date']
            # #     birth_date = datetime.strptime(birthday_text, '%Y-%m-%d')
            # # else:
            # #     birth_date = None
            # Artist.objects.create(
            #     name=name,
            #     real_name=real_name,
            #     nationality=nationality,
            #     birth_date=birth_date,
            #     constellation=constellation,
            #     blood_type=blood_type,
            # )
            return redirect('artist:artist-list')
    else:
        form = AritstForm()

    context = {
        'artist_form': form,
    }
    return render(request, 'artist/artist_add.html', context)
