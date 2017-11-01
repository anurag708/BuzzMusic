from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Comment)
admin.site.register(Feedback)
admin.site.register(Like)