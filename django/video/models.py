from django.db import models

from crawler.video import video_list_crawler


def dynamic_video_thumbnail_path(instance, filename):
    return f'video/{instance.video_id}/{filename}'


# class VideoManager(models.Manager):
#
#     def update_or_create_from_melon(self, video_id):
#
#         # result = video_list_crawler(keyword)
#         video, video_created = self.update_or_create(
#             video_id=video_id,
#             # defaults={
#             #     'video_id': result.video_id,
#             #     'title': result.title,
#             #     'thumbnails': result.thumbnails,
#             # }
#         )
#         return video, video_created


class Video(models.Model):

    video_id = models.CharField(
        'YouTube VideoId',
        max_length=100,
        unique=True,
    )
    title = models.CharField(
        'Video title',
        max_length=100,
    )
    thumbnail = models.ImageField(
        'Thumbnail image',
        upload_to=dynamic_video_thumbnail_path,
        blank=True,
    )

    # objects = VideoManager()

    def __str__(self):
        if self.thumbnail:
            return f'YouTube: {self.title}({self.video_id})[{self.thumbnail}]'
        else:
            return f'YouTube: {self.title}({self.video_id})'


