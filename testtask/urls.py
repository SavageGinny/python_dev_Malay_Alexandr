from django.contrib import admin
from django.urls import path
from UserActions.views import *

urlpatterns = [
    path('', user_data_view), #Домашняя страница
    path('admin/', admin.site.urls), #Админ панель
    path('api/comments/', comments, name='comments-api'), #API для получения данных о комментариях | GET http://127.0.0.1:8000/api/comments?login=<userloggin>
    path('api/general/', general, name='general-api'), #API для получения общей информации о действиях пользователя | GET http://127.0.0.1:8000/api/general?login=<userloggin>
    path("download_csv/<str:login>/<str:dataset_type>/", download_csv, name="download_csv"), #Ссылка на скачивание csv датасета

]
