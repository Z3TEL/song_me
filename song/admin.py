from django.contrib import admin
from song.models import *


admin.site.register(Author)
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Favorite)
