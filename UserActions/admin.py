from django.contrib import admin

from blogs.models import Blog, Post, User
from logs.models import EventType, Log, SpaceType

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(SpaceType)
admin.site.register(EventType)
admin.site.register(Log)