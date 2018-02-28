from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404

# from artist.models import Artist  -> import 위치 바뀜.
from artist.models.artist import Artist
from utils.file import download, get_buffer_ext
from video.models import Video


def video_list(request):
    pass


def video_add(request):
    if request.method == 'POST':
        # video_id = request.POST.get('video_id')
        #
        # video, _ = Video.objects.update_or_create_from_melon(video_id)
        #
        # # 1) 위에서 생성한 video를 Artist에 연결해주기위해
        # #    artist_detail.html에 artist의 pk를 이곳으로 전달.
        # # 2) 덤으로 기존에 있던 페이지로 redirect하는데도 써먹자
        # artist_pk = request.POST.get('artist_pk')
        # artist = get_object_or_404(Artist, pk=artist_pk)
        # artist.videos.add(video)
        #
        # return redirect('artist:artist-detail', artist_pk=artist_pk)

        video_id = request.POST.get('video_id')
        title = request.POST.get('title')
        thumbnails = request.POST.get('thumbnails')

        video, _ = Video.objects.update_or_create(
            video_id=video_id,
            defaults={
                'title': title,
                # 'thumbnail': thumbnails,
            }
        )

        # Artist에 video 넣어주기
        artist_pk = request.POST.get('artist_pk')
        artist = get_object_or_404(Artist, pk=artist_pk)
        artist.videos.add(video)


        print('')
        print(title)
        print(f'{title[:15]}')

        # 2) video 저

        # Video thumbnaili 사진저장
        temp_file = download(thumbnails)
        file_name = f'{title[:15]}.{get_buffer_ext(temp_file)}'
        video.thumbnail.save(file_name, File(temp_file))

        # next_path = request.POST.get(
        #     'next-path',
        #     reverse('artist:artist-detail', )
        # )

        return redirect('artist:artist-detail', artist_pk=artist_pk)
