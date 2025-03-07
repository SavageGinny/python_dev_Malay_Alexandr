from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models.functions import TruncDate
from django.db.models import Count, Q
from django.shortcuts import render
from django.http import HttpResponse
import csv
import requests
from .forms import *
from .serializers import *
from blogs.models import *
from logs.models import *

API_COMMENT_URL = "http://127.0.0.1:8000/api/comments"
API_GENERAL_URL = "http://127.0.0.1:8000/api/general"

def get_data_from_api(login):
    """
    Получает данные из двух API: для комментариев и общей активности пользователя.

    Args:
        login (str): Логин пользователя, для которого необходимо получить данные.

    Returns:
        tuple: Список комментариев и список общей активности пользователя.
            - comment_data (list): Список словарей с данными о комментариях пользователя.
            - general_data (list): Список словарей с общей активностью пользователя.
    """
    comment_response = requests.get(f"{API_COMMENT_URL}?login={login}")
    general_response = requests.get(f"{API_GENERAL_URL}?login={login}")

    comments = comment_response.json() if comment_response.status_code == 200 else []
    general = general_response.json() if general_response.status_code == 200 else []

    # Ищем данные для конкретного пользователя
    general_data = next((item["activities"] for item in general if item["user_login"] == login), [])

    return comments, general_data

def download_csv(request, login, dataset_type):
    """
    Формирует и отправляет CSV-файл с данными для пользователя.

    Args:
        request (HttpRequest): Запрос, который инициирует скачивание файла.
        login (str): Логин пользователя, для которого формируется файл.
        dataset_type (str): Тип данных для скачивания. Может быть:
            - "comments" — для скачивания данных о комментариях.
            - "general" — для скачивания общей активности пользователя.

    Returns:
        HttpResponse: Ответ с CSV-файлом, который будет отправлен пользователю для скачивания.
    """

    comment_data, general_data = get_data_from_api(login)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{login}_{dataset_type}.csv"'

    writer = csv.writer(response)

    if dataset_type == "comments":
        writer.writerow(["user_login", "post_header", "post_author", "comment count"])
        for comment in comment_data:
            writer.writerow([comment["login"], comment["header"], comment["author_login"], comment["comments_count"]])

    elif dataset_type == "general":
        writer.writerow(["date", "login_count", "logout_count", "blog_actions_count"])
        for activity in general_data:
            writer.writerow([activity["date"], activity["logins"], activity["logouts"], activity["blog_actions_count"]])

    return response

def user_data_view(request):
    """
    Обрабатывает запросы на страницу с данными пользователя. Получает данные о комментариях и общей активности
    пользователя из API и отображает их на странице. Также обрабатывает запросы на скачивание CSV-файлов.

    Args:
        request (HttpRequest): Запрос от клиента. Может содержать данные формы для ввода логина пользователя.

    Returns:
        HttpResponse: Ответ с рендером страницы, на которой отображаются данные пользователя и форма для ввода логина.
    """

    if request.method == "POST":
        form = InputUserLogin(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get("custom_login") or form.cleaned_data.get("input_login")
            comment_data, general_data = get_data_from_api(login)

            # Если нажата кнопка "Скачать"
            if "download_csv" in request.POST:
                dataset_type = request.POST["dataset_type"]
                return download_csv(login, dataset_type, comment_data, general_data)

            return render(request, "index.html", {
                "form": form,
                "comment_data": comment_data,
                "general_data": general_data
            })
    else:
        form = InputUserLogin()

    return render(request, "index.html", {"form": form})


@api_view(['GET'])
@permission_classes([AllowAny])
def comments(request):
    """
    Получает данные о комментариях пользователя из базы данных и возвращает их в формате JSON.

    Аргументы:
        request (HttpRequest): Запрос, содержащий логин пользователя.

    Возвращает:
        Response: Ответ с данными о комментариях пользователя в формате JSON, или ошибку, если логин не указан.
    """
    try:
        login = request.GET.get('login')

        comment_event = EventType.objects.using('logs_db').get(name="comment")
        user_id = User.objects.using('blogs_db').get(login=login).id

        logs = (
            Log.objects.using('logs_db')
            .filter(event_type=comment_event, user_id=user_id)
            .values('space_id')
            .annotate(comments_count=Count('id'))
        )

        post_ids = {log['space_id'] for log in logs}
        posts = {post.id: post.header for post in Post.objects.using('blogs_db').filter(id__in=post_ids)}

        author_ids = {post.author_id for post in Post.objects.using('blogs_db').filter(id__in=post_ids)}
        authors = {user.id: user.login for user in User.objects.using('blogs_db').filter(id__in=author_ids)}

        data = [
            {
                "login": login,
                "header": posts.get(log['space_id'], "Unknown"),
                "author_login": authors.get(
                    next((post.author_id for post in Post.objects.using('blogs_db').filter(id=log['space_id'])), None),
                    "Unknown"
                ),
                "comments_count": log["comments_count"],
            }
            for log in logs
        ]

        serializer = CommentsSerializer(data, many=True)
        return Response(serializer.data)
    except:
        return Response({'error': 'Login is required'}, status=400)
@api_view(['GET'])
@permission_classes([AllowAny])
def general(request):
    """
    Получает данные о входах, выходах и действиях пользователя в блоге из базы данных и возвращает их в формате JSON.

    Аргументы:
        request (HttpRequest): Запрос, содержащий логин пользователя.

    Возвращает:
        Response: Ответ с данными о действиях пользователя в формате JSON, или ошибку, если логин не указан.
    """
    try:
        login = request.GET.get('login')
        # ID для типов событий
        login_event = EventType.objects.using('logs_db').get(name="login")
        logout_event = EventType.objects.using('logs_db').get(name="logout")
        blog_space_type = SpaceType.objects.using('logs_db').get(name="blog")
        user_id = User.objects.using('blogs_db').get(login=login).id

        # Группируем логи по пользователю и дате
        logs = (
            Log.objects.using('logs_db')
            .annotate(date=TruncDate('datetime'))  # Обрезаем до даты (yyyy-mm-dd)
            .values('user_id', 'date')
            .annotate(
                logins=Count('id', filter=Q(event_type=login_event)),
                logouts=Count('id', filter=Q(event_type=logout_event)),
                blog_actions=Count('id', filter=Q(space_type=blog_space_type))
            )
            .filter(user_id=user_id)
        )
        # Формируем JSON в требуемом формате
        data = []
        for log in logs:
            user_login = login  # Получаем логин пользователя
            activity = {
                "date": log['date'],
                "logins": log['logins'],
                "logouts": log['logouts'],
                "blog_actions_count": log['blog_actions']
            }

            # Проверяем, есть ли уже такой пользователь в data
            user_exists = next((item for item in data if item["user_login"] == user_login), None)

            if user_exists:
                # Если пользователь найден, добавляем активность в его "activities"
                user_exists["activities"].append(activity)
            else:
                # Если пользователь не найден, добавляем новый объект с логином и первой активностью
                data.append({
                    "user_login": user_login,
                    "activities": [activity]  # Список активностей, т.к. activities - это many=True
                })
        serializer = UserActionsSerializer(data, many=True)
        return Response(serializer.data)
    except:
        return Response({'error': 'Login is required'}, status=400)