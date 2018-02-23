from io import BytesIO
from django.core.files import File
import requests

import magic
# from pathlib import Path


# def download(url, filename):
#
#     response = requests.get(url)
#     binary_data = response.content
#     # img_profile필드에 저장할 파일명을 전체 URL경로에서 추출 (Path라이브러리)
#     #         file_name = Path(url_img_cover).name
#     # print(f'file_name: {file_name}')
#
#     # 방법1 - 2/20 수업시간
#     # 파일처럼 취급되는 메모리 객체 temp_file를 생성
#     temp_file = BytesIO()
#
#     # temp_file에 이진데이터를 기록
#     temp_file.write(binary_data)
#
#     # 파일객체의 포인터를 시작부분으로 되돌림
#     temp_file.seek(0)
#
#     # 2/23
#     mime_type = magic.from_buffer(temp_file.read(), mime=True)
#     file_name = '{artist_id}.{ext}'.format(
#         artist_id=filename,
#         ext=mime_type.split('/')[-1]
#     )
#     # artist.img_profile.save(file_name, File(temp_file))
#
#     return file_name, temp_file


def download(url):

    response = requests.get(url)
    binary_data = response.content
    # img_profile필드에 저장할 파일명을 전체 URL경로에서 추출 (Path라이브러리)
    #         file_name = Path(url_img_cover).name
    # print(f'file_name: {file_name}')

    # 방법1 - 2/20 수업시간
    # 파일처럼 취급되는 메모리 객체 temp_file를 생성
    temp_file = BytesIO()

    # temp_file에 이진데이터를 기록
    temp_file.write(binary_data)

    # 파일객체의 포인터를 시작부분으로 되돌림
    temp_file.seek(0)

    # 2/23
    # mime_type = magic.from_buffer(temp_file.read(), mime=True)
    # file_name = '{artist_id}.{ext}'.format(
    #     artist_id=filename,
    #     ext=mime_type.split('/')[-1]
    # )
    # artist.img_profile.save(file_name, File(temp_file))

    # return file_name, temp_file
    return temp_file


def get_buffer_ext(buffer):
    buffer.seek(0)
    mime_info = magic.from_buffer(buffer.read(), mime=True)
    buffer.seek(0)
    return mime_info.split('/')[-1]