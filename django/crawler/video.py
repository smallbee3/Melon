import requests
from django.conf import settings

# from video.models import Video


def video_list_crawler(keyword):

    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'maxResults': 10,
        'type': 'video',
        'q': keyword,
    }

    # YouTube video list 출력
    response = requests.get(url, params)
    result_dict = response.json()

    video_info_list = []
    for i in range(10):
        video_id = result_dict['items'][i]['id'].get('videoId')
        title = result_dict['items'][i]['snippet']['title']
        thumbnails = result_dict['items'][i]['snippet']['thumbnails']['default']['url']
        from video.models import Video
        video_info_dict = {
            'video_id': video_id,
            'title': title,
            'thumbnails': thumbnails,
            # class VideoManager(models.Manager):
            # 에서 def update_or_create_from_melon(self, keyword):
            # 를 사용하기 위해 keyword 값도 넣어준다.
            # 'keyword': keyword,
            'is_exist': Video.objects.filter(video_id=video_id).exists(),

        }
        video_info_list.append(video_info_dict)

    return video_info_list
