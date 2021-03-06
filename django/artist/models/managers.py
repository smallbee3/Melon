import re
from datetime import datetime
from django.db import models

# 밖에 있는 이유는 클래스 안에 넣어도 상관은 없기도 하고.
# from artist.models.artist import Artist
from utils.file import download, get_buffer_ext


class ArtistManager(models.Manager):
    def update_or_create_from_melon(self, artist_id):
        from artist.models import Artist

###################### add_from_melon.py ######################

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

        # 예외처리 1
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

        # 예외처리 2 - 생년월일 없을 경우
        # if birth_date_str == '':
        #     birth_date = None
        # else:
        #     birth_date = datetime.strptime(birth_date_str, '%Y.%m.%d')

        # 예외처리 2-2 - 위의 4줄을 한 줄로 줄임
        # datetime.strptime(birth_date_str, '%Y.%m.%d') if birth_date_str else None,



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

        # response = requests.get(url_img_cover)

        # binary_data = response.content
# img_profile필드에 저장할 파일명을 전체 URL경로에서 추출 (Path라이브러리)
#         file_name = Path(url_img_cover).name
        # print(f'file_name: {file_name}')



        # 방법1 - 2/20 수업시간
# 파일처럼 취급되는 메모리 객체 temp_file를 생성
#         temp_file = BytesIO()

# temp_file에 이진데이터를 기록
#         temp_file.write(binary_data)

# 파일객체의 포인터를 시작부분으로 되돌림
#         temp_file.seek(0)

# artist.img_profile필드의 save를 따로 호출, 이름과 File객체를 전달
# (Django)File객체의 생성에는 (Python)File객체를 사용,
# 이때 (Python)File객체처럼 취급되는 BytesIO를 사용
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
        # 1)
        # artist, artist_created = Artist.objects.update_or_create(
        # 2) self.model이라는 이름으로 자신의 클래스에 접근가능
        # artist, artist_created = self.model.update_or_create(
        # 3) objects라는 것 자체가 매니저 객체였으니까 매니저 객체에 있는
        #    이 update_or_create를 그대로 실행하면 되는 거죠.
        #   (밖으로 나갔다가 다시 들어올 필요없이)
        artist, artist_created = self.update_or_create(

            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                # 'birth_date': birth_date,
                # 위의 예외처리 4줄 대신 '조건표현식' 한줄로 Pythonic하게!
                'birth_date': datetime.strptime(birth_date_str, '%Y.%m.%d') if birth_date_str else None,
                'constellation': constellation,
                'blood_type': blood_type,

                # 방법 3
                # 'img_profile': ContentFile(binary_data, name='test.jpg'),
                #  이런식으로 name에다가 값을 전달해주면 해당 값이 파일명이 됨.
                # 'img_profile': ContentFile(binary_data, name=file_name),

                # 방법 4
                # 'img_profile': img #-> 방법 4 쓴다면
            }
        )

        # 2/23
        # import magic
        #
        # mime_type = magic.from_buffer(temp_file.read(), mime=True)
        # file_name = '{artist_id}.{ext}'.format(
        #     artist_id=artist_id,
        #     ext=mime_type.split('/')[-1]
        # )

        # 위 코드를 utils/file.py로 분리함
        # 전달인자로 url과 artist_id를 전달함 (원래 두번째 인자는 artist_id는 아님)
        # file_name, temp_file = download(url_img_cover, artist_id)

# img_profile필드에 저장할 파일확장자를 바이너리 데이터 자체의 MIME_TYPE에서 가져옴
# 파일명은 artist_id를 사용
        temp_file = download(url_img_cover)
        file_name = '{artist_id}.{ext}'.format(
            artist_id=artist_id,
            ext=get_buffer_ext(temp_file),
        )


        # 2/23 - 사진 중복저장 방지 코드
        #       : 해당필드에 사진이 있는지 확인
        # 방법1 - 지우고 다시 만들기
        if artist.img_profile:
            artist.img_profile.delete()
        artist.img_profile.save(file_name, File(temp_file))

        # 방법2 - 있을경우 안만들기
        # if not artist.img_profile:
        #     artist.img_profile.save(file_name, File(temp_file))

        return artist, artist_created
        # 여기서 튜플로 전달해주기 때문에 받을 때도 튜플로 받아야함.
        # 안그러면 잘못된 int가 전달되었다는 500 에러가 발생.

        ###################### add_from_melon.py ######################
