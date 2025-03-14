from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('UserActions.urls')),
    path('admin/', admin.site.urls),
    path('api/comments/', include('UserActions.urls')),
    path('api/general/', include('UserActions.urls')),
    path("download_csv/<str:login>/<str:dataset_type>/", include('UserActions.urls')),
]
