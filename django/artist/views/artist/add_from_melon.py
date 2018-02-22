import re
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime

# from django.core.files.base import ContentFile
# from pathlib import Path

from ...models import Artist


__all__ = (
    'artist_add_from_melon',
)

def artist_add_from_melon(request):

    if request.method == 'POST':
        # print(request.POST)
        artist_id = request.POST.get('artist_id')


        ################# 크롤러 #################
        import requests
        from bs4 import BeautifulSoup
        url = f'https://www.melon.com/artist/detail.htm'
        params = {
            'artistId': artist_id,
        }
        response = requests.get(url, params)
        source = response.text
        soup = BeautifulSoup(source, 'lxml')

        # name
        name = soup.select_one('p.title_atist').strong.next_sibling

        # url_img_cover
        url_img = soup.select_one('span#artistImgArea > img').get('src')
        url_img_cover = re.search(r'(.*.jpg)', url_img).group(1)


        # real_name, nationality, birth_date, constellation, blood_type
        personal_information = {}
        if re.search(r'신상정보</h3>', source, re.DOTALL):
            dl_list = re.search(r'신상정보</h3>.*?-->(.*?)</dl>', source, re.DOTALL)
            # dt = re.findall('<dt>.*?</dt>', dl_list.group(1))
            # dd = re.findall('<dd>.*?</dd>', dl_list.group(1))
            soup = BeautifulSoup(dl_list.group(), 'lxml')
            dt = soup.select('dt')
            dd = soup.select('dd')

            dd_dt = list(zip(dt, dd))
            # print(dd_dt)

            for i, j in dd_dt:
                i = i.get_text(strip=True)
                j = j.get_text(strip=True)
                personal_information[i] = j
            # print(self._personal_information)
        else:
            personal_information = ''
        #######################################



        # url_img_cover = artist.url_img_cover
        real_name = personal_information.get('본명', '')
        nationality = personal_information.get('국적', '')
        birth_date_str = personal_information.get('생일', '')
        constellation = personal_information.get('별자리', '')
        blood_type = personal_information.get('혈액형', '')

        # 튜플의 리스트를 순회하며 blood_type을 결정
        for short, full in Artist.CHOICES_BLOOD_TYPE:
            if blood_type.strip() == full:
                blood_type = short
                break
        else:
            # break가 발생하지 않은 경우
            # (미리 정의해놓은 혈액형 타입에 없을 경우)
            # 기타 혈액형값으로 설정
            blood_type = Artist.BLOOD_TYPE_OTHER

        # 생년월일 없을 경우
        if birth_date_str == '':
            birth_date = None
        else:
            birth_date = datetime.strptime(birth_date_str, '%Y.%m.%d')



        # 1단계 - Artist 생성
        # Artist.objects.create(
        #     melon_id=artist_id,
        #     name=name,
        #     real_name=real_name,
        #     nationality=nationality,
        #     birth_date=datetime.strptime(birth_date_str, '%Y.%m.%d'),
        #     constellation=constellation,
        #     blood_type=blood_type,
        # )


        # artist_id가 melon_id에 해당하는 Artist가 이미 있다면
        # 해당 Artist의 내용을 update,
        # 없으면 Artist를 생성

        # 2단계 - 코드가 두번 반복됨, 암걸릴 것 같음.
        # if Artist.objects.filter(melon_id=artist_id).exists():
        #     artist = Artist.objects.get(melon_id=artist_id)
        #     artist.melon_id = artist_id
        #     artist.name = name
        #     artist.real_name = real_name
        #     artist.nationality = nationality
        #     artist.birth_date = datetime.strptime(birth_date_str, '%Y.%m.%d')
        #     artist.constellation = constellation
        #     artist.blood_type = blood_type
        #     artist.save()
        # else:
        #     Artist.objects.create(
        #         melon_id=artist_id,
        #         name=name,
        #         real_name=real_name,
        #         nationality=nationality,
        #         birth_date=datetime.strptime(birth_date_str, '%Y.%m.%d'),
        #         constellation=constellation,
        #         blood_type=blood_type,
        #     )


        # 3단계 - get_or_create() 사용
        # artist, artist_created = Artist.objects.get_or_create(melon_id=artist_id)
        # artist.name = name
        # artist.real_name = real_name
        # artist.nationality = nationality
        # artist.birth_date = datetime.strptime(birth_date_str, '%Y.%m.%d')
        # artist.constellation = constellation
        # artist.blood_type = blood_type
        # artist.save()
        # return redirect('artist:artist-list')

        # -> 문제점: save()가 두번 발생함. 이미 존재하면 가져오고
        #     속성을 변경하고 save()를 하면 되는데, created할 때는
        #     객체를 만들 때 save()를 한번 하고 밑에서 또 한번 save()를 함.


        ######## Save file to ImageField ########
        from io import BytesIO
        from pathlib import Path
        from django.core.files import File
        from django.core.files.base import ContentFile

        response = requests.get(url_img_cover)
        binary_data = response.content

        file_name = Path(url_img_cover).name

        # print(f'file_name: {file_name}')

        # 방법1 - 2/20 수업시간
        # temp_file = BytesIO()
        # temp_file.write(binary_data)
        # temp_file.seek(0)

        # artist.img_profile.save(file_name, File(temp_file))
        # -> update_or_create에서 반환된 obj인 'artist'를 활용하기 때문에
        #    이 방법1 을 실행하려면 아래쪽으로 이동시킬 것.


        # 방법2 - ContentFile이용 by che1
        #
        # artist.img_profile.save(file_name, ContentFile(binary_data))
        # -> update_or_create에서 반환된 obj인 'artist'를 활용하기 때문에
        #    이 방법2 를 실행하려면 아래쪽으로 이동시킬 것.

        # 방법 3 - update_or_create 이용해서 이미지 저장하기
        #
        # 아래에서
        # 'img_profile': ContentFile(binary_data, name='test.jpg'),
        # 이 부분이 방법 3


        # 방법 4 - 위 방법으로 사진 중복저장을 막지 못해서 이 방법 4 생각해냄.
        # if (파일이 안같으면):
        #   기존 사진 지우는 코드 (기존 사진에서 업데이트 되었으므로)
        #   img = ContentFile(binary_data, filename)
        # else: (파일이 같으면)
        #   pass


        # 4단계 -update_or_create() 사용
        artist, created = Artist.objects.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': birth_date,
                'constellation': constellation,
                'blood_type': blood_type,

                # 방법 3
                # 'img_profile': ContentFile(binary_data, name='test.jpg'),
                #  이런식으로 name에다가 값을 전달해주면 해당 값이 파일명이 됨.
                'img_profile': ContentFile(binary_data, name=file_name),

                # 방법 4
                # 'img_profile': img #-> 방법 4 쓴다면
            }
        )


    # 테스트 출력
    # return HttpResponse(url_img_cover)
    return redirect('artist:artist-list')