from django.contrib import admin
from logs.models import SpaceType, EventType, Log
from blogs.models import User, Blog, Post

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(SpaceType)
admin.site.register(EventType)
admin.site.register(Log)