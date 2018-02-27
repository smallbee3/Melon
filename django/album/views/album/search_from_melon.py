# from django.shortcuts import render
#
# __all__ = (
#     'album_search_from_melon',
# )
#
#
# def album_search_from_melon(request):
#
#     q = request.GET.get('keyword')
#
#     result = song_list_crawler(q)
#     context = {
#         "result": result,
#     }
#     return render(request, 'song/album_search_from_melon.html', context)
